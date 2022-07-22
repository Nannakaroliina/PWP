from flask_restful import Resource

from src.models.producer import Producer
from src.schemas.schemas import ProducerSchema

producer_schema = ProducerSchema()
producer_list_schema = ProducerSchema(many=True)


class ProducerList(Resource):
    @classmethod
    def get(cls):
        return {"producers": producer_list_schema.dump(Producer.find_all())}, 200


    @classmethod
    def get(cls, name):
        db_producer = Producer.find_by_name(name)
        return producer_schema.dump(db_producer)
