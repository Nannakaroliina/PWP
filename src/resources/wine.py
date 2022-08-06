import json
from sqlite3 import IntegrityError
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from src.libs.helpers import check_file_and_proper_naming, upload_file
from src.models.wine import Wine
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.wine_type import Wine_type
from src.schemas.schemas import GrapeSchema, ProducerSchema, WineSchema

from src.utils.constants import \
    ALREADY_EXISTS, NOT_JSON, ERROR_INSERTING, ERROR_DELETING

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
        file = request.files.get('file')
        try:
            content = json.loads(request.form.get('data'))
        except BadRequest:
            return {"[ERROR]": NOT_JSON}, 400

        if file:
            if check_file_and_proper_naming(file):
                file_url = upload_file(file)
                content["picture"] = file_url

        try:
            wine = wine_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Wine.find_by_name(content["name"]):
            return {"[INFO]": ALREADY_EXISTS}, 409

        # checking if the user included wine_type
        if "wine_type" in content:

            wine_type = Wine_type.find_by_type(wine.wine_type.type)

            if wine_type:
                wine.wine_type = None
                wine.wine_type = wine_type

        # checking if grape included
        if "grape" in content:

            grape = Grape.find_by_name(wine.grape.name)

            if grape:
                wine.grape = None
                wine.grape = grape

        # checking if producer included
        if "producer" in content:

            producer = Producer.find_by_name(wine.producer.name)

            if producer:
                wine.producer = None
                wine.producer = producer

        try:
            wine.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

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
        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except:   
                return {"[ERROR]": ERROR_DELETING}, 500
        
        return {"[ERROR]": "Wine {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def put(cls, name):
        file = request.files.get('file')
        try:
            content = json.loads(request.form.get('data'))
        except BadRequest:
            return {"[ERROR]": NOT_JSON}, 400

        item = Wine.find_by_name(name)
        try:
            if "name" not in content:
                content["name"] = item.name
            wine = wine_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if item:
            if wine.name:
                item.name = wine.name

            if wine.wine_type:
                try:
                    wine_type = Wine_type.find_by_type(wine.wine_type.type)
                    item.wine_type_id = wine_type.id
                except AttributeError:
                    return{"[ERROR]": "Wine_type not found"}
            
            if wine.style:
                item.style = wine.style

            if wine.description:
                item.description = wine.description

            if wine.grape:
                try:
                    grape = Grape.find_by_name(wine.grape.name)
                    item.grape_id = grape.id
                except AttributeError:
                    return {"[ERROR]": "Grape not found"}, 400

            if wine.producer:
                try:
                    producer = Producer.find_by_name(wine.producer.name)
                    item.producer_id = producer.id
                except AttributeError:
                    return {"ERROR": "Producer not found"}, 400
                
            if wine.year_produced:
                item.year_produced = wine.year_produced
            
            if wine.alcohol_percentage:
                item.alcohol_percentage = wine.alcohol_percentage
            
            if wine.volume:
                item.volume = wine.volume
            
            if file:
                if check_file_and_proper_naming(file):
                    file_url = upload_file(file)
                    item.picture = file_url
        
        else:
            return {"[ERROR]": "Wine not found"}, 400
            
        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return wine_schema.dump(item), 200
