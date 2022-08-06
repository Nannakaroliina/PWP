import logging
import os
import re
import requests

from typing import Union
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.libs.aws import AwsBucket
from src.utils.constants import ALLOWED_EXTENSIONS

s3 = AwsBucket()


def check_file_and_proper_naming(file: Union[str, FileStorage]) -> bool:
    """
    Check if a filename match the given regex and is in allowed format
    """
    filename = secure_filename(file.filename)

    allowed_format = "|".join(ALLOWED_EXTENSIONS)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def upload_file(file: Union[str, FileStorage]):
    key = file.filename

    # check if file doesn't exist and create temp file under static folder
    if not os.path.exists('static/' + key):
        file.save('static/' + key)

    if s3.check_if_file_exists(key):
        # remove temp file since the image exists already
        os.remove('static/' + key)
        logging.info('File already exists, returning url')
        return get_file_url(key)
    else:
        response = s3.create_presigned_post(file_name=key)
        if response is None:
            return {"[ERROR]": "Response was empty, try again"}, 400

        files = [('file', open('static/' + key, 'rb'))]

        upload_response = requests.post(response['url'], data=response['fields'], files=files)

        if upload_response.status_code == 204:
            # remove temp file
            os.remove('static/' + key)
            logging.info('File successfully uploaded to S3')
            return get_file_url(key)
        elif upload_response.status_code == 500:
            return {"[ERROR]": "Unexpected error occurred"}, 500
        else:
            return {"[ERROR]": "Request was unsuccessful"}, 400


def get_file_url(filename: str):
    return s3.get_file_url(file_name=filename)


def get_all_file_urls():
    return s3.get_file_urls()
