
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

from src.utils.constants import \
     ALREADY_EXISTS, NOT_JSON, ERROR_INSTERTING, ERROR_DELETING

grape_schema = GrapeSchema()
producer_schema = ProducerSchema()
wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


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
            return {"message": ALREADY_EXISTS}, 409

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

        #checking if producer included
        if "producer" in content:

            producer = Producer.find_by_name(wine.producer.name)

            if producer:
                wine.producer = None
                wine.producer = producer

        try:
            wine.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSTERTING}, 500

        return wine_schema.dump(wine), 201


class WineItem(Resource):

    @classmethod
    def get(cls, name):
        db_wine = Wine.find_by_name(name)
        return wine_schema.dump(db_wine)

    @classmethod
    @jwt_required()
    def delete(cls, name):

        item = Wine.find_by_name(name)
        print(item)
        if item:
            try:
                item.delete()
                return {"message": "{} deleted".format(item.name)}, 200
            except:   
                return {"[ERROR]": ERROR_DELETING}, 500
        
        return {"[ERROR]": "Wine {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def put(cls, name):

        if not request.is_json:
            return {"message": NOT_JSON}, 415
        
        content = request.get_json()

        item = Wine.find_by_name(name)

        if item:
            item.name = content["name"]

            if "wine_type" in content:
                try:
                    wine_type = Wine_type.find_by_type(content["wine_type"]["type"])
                    item.wine_type_id = wine_type.id
                except AttributeError:
                    return{"[ERROR]": "Wine_type not found"}
            
            if "style" in content:
                item.style = content["style"]

            if "description" in content:
                item.description = content["description"]

            if "grape" in content:
                try:
                    grape = Grape.find_by_name(content["grape"]["name"])
                    item.grape_id = grape.id
                except AttributeError:
                    return {"[ERROR]": "Grape not found"}, 400

            if "producer" in content:
                try:
                    producer = Producer.find_by_name(content["producer"]["name"])
                    item.producer_id = producer.id
                except AttributeError:
                    return {"ERROR": "Producer not found"}, 400
                
            if "year_produced" in content:
                item.year_produced = content["year_produced"]
            
            if "alcohol_percentage" in content:
                item.alcohol_percentage = content["alcohol_percentage"]
            
            if "volume" in content:
                item.volume = content["volume"]
            
            if "picture" in content:
                item.picture = content["picture"]
        
        else:
            return {"[ERROR]": "Wine not found"}, 400

        try:
            item = wine_schema.load(content)
        except ValidationError as err:
            return err.messages, 400
            
        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSTERTING}, 500

        return wine_schema.dump(item), 200
