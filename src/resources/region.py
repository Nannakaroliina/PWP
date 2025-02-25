"""
Module for region resource. Provides the methods to get, post, patch and delete
data related to region. Some methods are jwt restricted.
"""
from sqlite3 import IntegrityError, InternalError
from urllib import request

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from src.models.region import Region
from src.models.country import Country
from src.schemas.schemas import CountrySchema, RegionSchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSERTING, NOT_JSON, NOT_FOUND, BAD_REQUEST

country_schema = CountrySchema()
region_schema = RegionSchema()
region_list_schema = RegionSchema(many=True)


# noinspection DuplicatedCode
class RegionList(Resource):
    """
    Class that provides the methods to get regions and post new regions.
    """
    @classmethod
    def get(cls):
        """
        Get a list of regions from database
        :return: List of regions
        """
        try:
            return {"regions": region_list_schema.dump(Region.find_all())}, 200
        except BadRequest:
            return {"[ERROR]": BAD_REQUEST}, 400

    @classmethod
    @jwt_required()
    def post(cls):
        """
        Post a new region to database, takes a json from request
        which is used to create new Region object to add to db

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "name": "region",
            "country" {  # Optional
                "name": "country"
            }
        }

        :return: Serialized Region object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        try:
            region = region_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Region.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        # check if user included country
        if "country" in content:

            country = Country.find_by_name(region.country.name)

            if country:
                region.country = None
                region.country = country

        try:
            region.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return region_schema.dump(region), 201

    
class RegionItem(Resource):
    """
    Class that provides the methods to get, delete and patch region.
    """
    @classmethod
    def get(cls, name):
        """
        Get one specific region from database with given name
        :param name: string name for region
        :return: Serialized Region object as a JSON
        """
        db_region = Region.find_by_name(name)
        if db_region is not None:
            return region_schema.dump(db_region), 200
        else:
            return {"[INFO]": NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def delete(cls, name):
        """
        Delete one specific region from database with given name
        Headers: Authorization: Bearer access token

        :param name: string name for region
        :return: string info
        """
        item = Region.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except InternalError:
                return {"[ERROR]": ERROR_DELETING}, 500

        return {"[ERROR]": "Region {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def patch(cls, name):
        """
        Update the existing region in the database by given name.
        Takes a json data from request.

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "name": "producer",
            "description": "Optional description",
            "region" {  # Optional
                "name": "region"
            }
        }

        :param name: string name of the region
        :return: Serialized Region object as a JSON
        """
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()
        item = Region.find_by_name(name)

        if item:
            try:
                if "name" not in content:
                    content["name"] = item.name
                region = region_schema.load(content)
            except ValidationError as err:
                return err.messages, 400

            item.name = region.name

            if region.country:
                try:
                    country = Country.find_by_name(region.country.name)
                    item.country_id = country.id
                except AttributeError:
                    return {"[ERROR]": "Country not found"}, 404
        else:
            return {"[ERROR]": "Region not found"}, 404

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500
        
        return region_schema.dump(item), 200
