from sqlite3 import IntegrityError

from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request

from src.models.wine_type import Wine_type
from src.schemas.schemas import WineTypeSchema
from src.utils.constants import NOT_JSON, ERROR_INSERTING

wine_type_schema = WineTypeSchema()
wine_type_list_schema = WineTypeSchema(many=True)


class Wine_typeList(Resource):
    @classmethod
    def get(cls):
        return {"wine_types": wine_type_list_schema.dump(Wine_type.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        if not request.json:
            return {"[INFO]": NOT_JSON}, 415

        json_item = request.get_json()

        if not json_item["type"]:
            return {"[INFO]": "Wine type can't be empty"}, 400

        # try to validate the winetype
        try:
            item = wine_type_schema.load(json_item)
        except ValidationError as err:
            return err.messages, 400

        # check if the type already exist in db
        if Wine_type.find_by_type(request.json["type"]):
            return {"[INFO]": "Wine type already exits"}, 409

        # try add new type to db
        try:
            item.add()
        except IntegrityError as err:
            return {"[ERROR]": ERROR_INSERTING}, 400

        return wine_type_schema.dumps(item), 201


class Wine_typeItem(Resource):
    @classmethod
    def get(cls, name):
        db_wine_type = Wine_type.find_by_type(name)
        return wine_type_schema.dump(db_wine_type)
