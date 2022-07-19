from os import environ
from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    """Base app config"""
    DEBUG = True

    # Database configs
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///../db/winebase.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS configs
    AWS_BUCKET = environ.get("AWS_BUCKET")
    ACCESS_KEY_ID = environ.get("ACCESS_KEY_ID")
    ACCESS_KEY_SECRET = environ.get("ACCESS_KEY_SECRET")