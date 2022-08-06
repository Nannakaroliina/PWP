from sqlite3 import IntegrityError

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.models.grape import Grape
from src.models.region import Region
from src.schemas.schemas import GrapeSchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSERTING, NOT_JSON

grape_schema = GrapeSchema()
grape_list_schema = GrapeSchema(many=True)


class GrapeList(Resource):

    @classmethod
    def get(cls):
        return {"grapes": grape_list_schema.dump(Grape.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        try: 
            grape = grape_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Grape.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        #checking if the user included region
        if "region" in content:

            region = Region.find_by_type(grape.region.name)

            if region:
                grape.region = None
                grape.region = region

        try:
            grape.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return grape_schema.dump(grape), 201


class GrapeItem(Resource):

    @classmethod
    def get(cls, name):
        db_grape = Grape.find_by_name(name)
        return grape_schema.dump(db_grape)

    @classmethod
    @jwt_required()
    def delete(cls, name):

        item = Grape.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except:
                return {"[ERROR]": ERROR_DELETING}, 500
        
        return {"[ERROR]": "Grape {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def put(cls, name):

        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        item = Grape.find_by_name(name)

        if item:
            item.name = content["name"]

            if "region" in content:
                try:
                    region = Region.find_by_name(content["region"]["name"])
                    item.region_id = region.id
                except AttributeError:
                    return {"[ERROR]": "Region not found"}, 404

            if "description" in content:
                item.description = content["description"]
        else:
            return {"[ERROR]": "Grape not found"}, 404

        try: 
            item = grape_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return grape_schema.dump(item), 200