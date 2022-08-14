"""
Configuration file to provide the app configuration
"""
from os import environ
from dotenv import load_dotenv

from src.schemas.schemas import WineSchema, UserSchema, WineTypeSchema, GrapeSchema, ProducerSchema, RegionSchema, \
    CountrySchema

load_dotenv(".env")


class Config:
    """Base app config"""
    DEBUG = True

    # Database configs
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS configs
    AWS_BUCKET = environ.get("AWS_BUCKET")
    ACCESS_KEY_ID = environ.get("ACCESS_KEY_ID")
    ACCESS_KEY_SECRET = environ.get("ACCESS_KEY_SECRET")

    # Authentication
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")

    # Redoc
    REDOC = {'title': 'Winetime',
             'marshmallow_schemas': [UserSchema, WineSchema, WineTypeSchema, GrapeSchema,
                                     ProducerSchema, RegionSchema, CountrySchema],
             'version': '0.0.1',
             'openapi_version': '3.0.3'}
