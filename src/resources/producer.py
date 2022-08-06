from sqlite3 import IntegrityError

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.models.producer import Producer
from src.models.region import Region
from src.schemas.schemas import ProducerSchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSERTING, NOT_JSON

producer_schema = ProducerSchema()
producer_list_schema = ProducerSchema(many=True)


# noinspection DuplicatedCode
class ProducerList(Resource):
    
    @classmethod
    def get(cls):
        return {"producers": producer_list_schema.dump(Producer.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):
        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415
        
        content = request.get_json()

        try:
            producer = producer_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Producer.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        # check if user included region
        if "region" in content:

            region = Region.find_by_name(producer.region.name)
        
            if region:
                producer.region = None
                producer.region = region

        try:
            producer.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return producer_schema.dump(producer), 201


class ProducerItem(Resource):

    @classmethod
    def get(cls, name):

        db_producer = Producer.find_by_name(name)
        return producer_schema.dump(db_producer)

    @classmethod
    @jwt_required()
    def delete(cls, name):

        item = Producer.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"[INFO]": "{} deleted".format(item.name)}, 200
            except:
                return {"[ERROR]": ERROR_DELETING}, 500

        return {"[ERROR]": "Producer {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def put(cls, name):

        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        item = Producer.find_by_name(name)

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
            return {"[ERROR]": "Producer {} not found".format(name)}, 404

        try:
            item = producer_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSERTING}, 500

        return producer_schema.dump(item), 200
