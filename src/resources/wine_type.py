"""
Module for wine type resource. Provides the methods to get, post, patch and delete
data related to wine type. Some methods are jwt restricted.
"""
from sqlite3 import IntegrityError, InternalError

from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request

from src.models.wine_type import Wine_type
from src.schemas.schemas import WineTypeSchema
from src.utils.constants import NOT_JSON, ERROR_INSERTING, NOT_FOUND, ERROR_DELETING

wine_type_schema = WineTypeSchema()
wine_type_list_schema = WineTypeSchema(many=True)


# noinspection DuplicatedCode
class Wine_typeList(Resource):
    """
    Class that provides the methods to get wine types and post new wine types.
    """
    @classmethod
    def get(cls):
        """
        Get a list of wine types from database
        :return: List of wine types
        """
        return {"wine_types": wine_type_list_schema.dump(Wine_type.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        """
        Post a new wine type to database, takes a json from request
        which is used to create new Wine_type object to add to db

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "type": "wine type"
        }

        :return: Serialized Wine_type object as a JSON
        """
        if not request.json:
            return {"[INFO]": NOT_JSON}, 415

        json_item = request.get_json()

        # try to validate the wine type
        try:
            item = wine_type_schema.load(json_item)
        except ValidationError as err:
            return err.messages, 400

        # check if the type already exist in db
        if Wine_type.find_by_type(request.json["type"]):
            return {"[INFO]": "Wine type already exits"}, 409

        # try to add new type to db
        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return wine_type_schema.dump(item), 201


class Wine_typeItem(Resource):
    """
    Class that provides the methods to get, delete and patch wine type.
    """
    @classmethod
    def get(cls, name):
        """
        Get one specific wine type from database with given name
        :param name: string name for wine type
        :return: Serialized Wine_type object as a JSON
        """
        db_wine_type = Wine_type.find_by_type(name)
        if db_wine_type is not None:
            return wine_type_schema.dump(db_wine_type), 200
        else:
            return {"[INFO]": NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def delete(cls, name):
        """
        Delete one specific wine type from database with given name
        Headers: Authorization: Bearer access token

        :param name: string name for wine type
        :return: string info
        """
        item = Wine_type.find_by_type(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.type)}, 200
            except InternalError:
                return {"[ERROR]": ERROR_DELETING}, 500

        return {"[ERROR]": "Wine_type {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def patch(cls, name):
        """
        Update the existing wine type in the database by given name.

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "type": "wine type"
        }

        :param name: string name of the wine type
        :return: Serialized Wine_type object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()
        item = Wine_type.find_by_type(name)

        if item:
            try:
                wine_type = wine_type_schema.load(content)
            except ValidationError as err:
                return err.messages, 400

            item.type = wine_type.type
        else:
            return {"[ERROR]": "Wine type not found"}, 404

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return wine_type_schema.dump(item), 200
