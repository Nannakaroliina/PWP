
from sqlite3 import IntegrityError
import traceback
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request, Response, url_for
from marshmallow import ValidationError

from src.models.wine import Wine
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.wine_type import Wine_type
from src.schemas.schemas import GrapeSchema, ProducerSchema, WineSchema

grape_schema = GrapeSchema()
producer_schema = ProducerSchema()
wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)

NOT_JSON = "Request must be JSON"
ERROR_INSTERING = "Could not add to database"


class WineList(Resource):

    @classmethod
    def get(cls):
        return {"wines": wine_list_schema.dump(Wine.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        if not request.is_json:
            return {"message": NOT_JSON}, 415
        
        content = request.get_json()
        try:
            wine = wine_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Wine.find_by_name(content["name"]):
            return {"message": "Wine already exists"}, 409

        #checking if the user included wine_type
        if "wine_type" in content:

            wine_type = Wine_type.find_by_type(wine.wine_type.type)

            if wine_type:
                wine.wine_type = None
                wine.wine_type = wine_type

        #checking if grape included
        if "grape" in content:

            grape = Grape.find_by_name(wine.grape.name)

            if grape:
                wine.grape = None
                wine.grape = grape

        try:
            wine.add()
        except IntegrityError as e:
            return {"messages": e}, 500

        return wine_schema.dump(wine), 201

class WineItem(Resource):
    @classmethod
    def get(cls, name):
        db_wine = Wine.find_by_name(name)
        return wine_schema.dump(db_wine)
