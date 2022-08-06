import logging
import boto3
from botocore.exceptions import ClientError
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

    def get_file_url(self, file_name):
        try:
            public_url = self.s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket, 'Key': file_name},
                                                        ExpiresIn=604800)
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
                                                               ExpiresIn=604800)
                public_urls.append(presigned_url)
                return public_urls
        except ClientError as e:
            logging.error(e)
            return None

    def check_if_file_exists(self, file_name):
        try:
            self.s3.head_object(Bucket=self.bucket, Key=file_name)
            return True
        except ClientError as e:
            logging.error(e)
            return False
