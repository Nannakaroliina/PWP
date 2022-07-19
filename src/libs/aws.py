import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from werkzeug.utils import secure_filename
from config import Config


class AwsBucket:

    def __init__(self, bucket_name=None):
        self.bucket = bucket_name or Config.AWS_BUCKET
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.ACCESS_KEY_ID,
            aws_secret_access_key=Config.ACCESS_KEY_SECRET
        )

    def create_presigned_post(self, file_name,
                              fields=None, conditions=None, expiration=3600):
        try:
            response = self.s3.generate_presigned_post(self.bucket,
                                                       file_name,
                                                       Fields=fields,
                                                       Conditions=conditions,
                                                       ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None
        return response

    def upload_to_aws(self, file, acl="public-read"):
        filename = secure_filename(file.filename)
        try:
            self.s3.upload_fileobj(file,
                                   self.bucket,
                                   file.filename,
                                   ExtraArgs={"ACL": acl, "ContentType": file.content_type}
                                   )
        except NoCredentialsError:
            print("Credentials not available")
        except Exception as e:
            print("Something Happened: ", e)
            return e

        return file.filename

    def get_file_url(self, file_name):
        try:
            public_url = self.s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket, 'Key': file_name},
                                                        ExpiresIn=3600)
            return public_url
        except ClientError as e:
            logging.error(e)
            return None

    def get_file_urls(self):
        public_urls = []
        try:
            for item in self.s3.list_objects(Bucket=self.bucket)['Contents']:
                presigned_url = self.s3.generate_presigned_url('get_object',
                                                               Params={'Bucket': self.bucket, 'Key': item['Key']},
                                                               ExpiresIn=3600)
                public_urls.append(presigned_url)
                return public_urls
        except ClientError as e:
            logging.error(e)
            return None
