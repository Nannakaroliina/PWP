"""
Module for country resource. Provides the methods to get, post, patch and delete
data related to country. Some methods are jwt restricted.
"""
from sqlite3 import IntegrityError, InternalError

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from src.models.country import Country
from src.schemas.schemas import CountrySchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSERTING, NOT_JSON, NOT_FOUND, BAD_REQUEST

country_schema = CountrySchema()
country_list_schema = CountrySchema(many=True)


# noinspection DuplicatedCode
class CountryList(Resource):
    """
    Class that provides the methods to get countries and post new countries.
    """
    @classmethod
    def get(cls):
        """
        Get a list of countries from database
        :return: List of countries
        """
        try:
            return {"countries": country_list_schema.dump(Country.find_all())}, 200
        except BadRequest:
            return {"[ERROR]": BAD_REQUEST}, 400

    @classmethod
    @jwt_required()
    def post(cls):
        """
        Post a new country to database, takes a json from request
        which is used to create new Country object to add to db

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example:
        {
            "name": "country"
        }

        :return: Serialized Country object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        try:
            country = country_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Country.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        try:
            country.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return country_schema.dump(country), 201


class CountryItem(Resource):
    """
    Class that provides the methods to get, delete and patch country.
    """
    @classmethod
    def get(cls, name):
        """
        Get one specific country from database with given name
        :param name: string name for country
        :return: Serialized Country object as a JSON
        """
        db_country = Country.find_by_name(name)
        if db_country is not None:
            return country_schema.dump(db_country), 200
        else:
            return {"[INFO]": NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def delete(cls, name):
        """
        Delete one specific country from database with given name
        Headers: Authorization: Bearer access token

        :param name: string name for country
        :return: string info
        """
        item = Country.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except InternalError:
                return {"[ERROR]": ERROR_DELETING}, 500

        return {"[ERROR]": "Country {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def patch(cls, name):
        """
        Update the existing country in the database by given name.

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example:
        {
            "type": "wine type"
        }

        :param name: string name of the wine type
        :return: Serialized Country object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()
        item = Country.find_by_name(name)

        if item:
            try:
                country = country_schema.load(content)
            except ValidationError as err:
                return err.messages, 400

            item.name = country.name
        else:
            return {"[ERROR]": "Country not found"}, 404

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return country_schema.dump(item), 200
