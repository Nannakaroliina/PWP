"""
Module for grape resource. Provides the methods to get, post, patch and delete
data related to grape. Some methods are jwt restricted.
"""
from sqlite3 import IntegrityError, InternalError

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.models.grape import Grape
from src.models.region import Region
from src.schemas.schemas import GrapeSchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSERTING, NOT_JSON, NOT_FOUND

grape_schema = GrapeSchema()
grape_list_schema = GrapeSchema(many=True)


# noinspection DuplicatedCode
class GrapeList(Resource):
    """
       Class that provides the methods to get grapes and post new grape.
    """
    @classmethod
    def get(cls):
        """
        Get a list of grapes from database
        :return: List of grapes
        """
        return {"grapes": grape_list_schema.dump(Grape.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        """
        Post a new grape to database, takes a json from request
        which is used to create new Grape object to add to db

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "name": "grape",
            "description": "Optional description",
            "region" {  # Optional
                "name": "region"
            }
        }

        :return: Serialized Grape object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        try: 
            grape = grape_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Grape.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        # checking if the user included region
        if "region" in content:

            region = Region.find_by_name(grape.region.name)

            if region:
                grape.region = None
                grape.region = region

        try:
            grape.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return grape_schema.dump(grape), 201


class GrapeItem(Resource):
    """
    Class that provides the methods to get, delete and patch grape.
    """
    @classmethod
    def get(cls, name):
        """
        Get one specific grape from database with given name
        :param name: string name for grape
        :return: Serialized Grape object as a JSON
        """
        db_grape = Grape.find_by_name(name)
        if db_grape is not None:
            return grape_schema.dump(db_grape), 200
        else:
            return {"[INFO]": NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def delete(cls, name):
        """
        Delete one specific grape from database with given name
        Headers: Authorization: Bearer access token

        :param name: string name for grape
        :return: string info
        """
        item = Grape.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except InternalError:
                return {"[ERROR]": ERROR_DELETING}, 500
        
        return {"[ERROR]": "Grape {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def patch(cls, name):
        """
        Update the existing grape in the database by given name.
        Takes a json data from request.

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "name": "grape",
            "description": "Optional description",
            "region" {  # Optional
                "name": "region"
            }
        }

        :param name: string name of the grape
        :return: Serialized Grape object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()
        item = Grape.find_by_name(name)

        if item:
            try:
                if "name" not in content:
                    content["name"] = item.name
                grape = grape_schema.load(content)
            except ValidationError as err:
                return err.messages, 400

            item.name = grape.name

            if grape.region:
                try:
                    region = Region.find_by_name(grape.region.name)
                    item.region_id = region.id
                except AttributeError:
                    return {"[ERROR]": "Region not found"}, 404

            if grape.description:
                item.description = grape.description
        else:
            return {"[ERROR]": "Grape not found"}, 404

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return grape_schema.dump(item), 200
