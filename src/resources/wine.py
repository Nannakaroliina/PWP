import json

from flask_restful import Resource

from src.models.wine import Wine


class WineList(Resource):
    @classmethod
    def get(cls):
        return {"wines":[wine.serialize() for wine in Wine.find_all()]}, 200

class WineItem(Resource):
    @classmethod
    def get(cls, name):
        db_wine = Wine.find_by_name(name)
        return db_wine.serialize(), 200
