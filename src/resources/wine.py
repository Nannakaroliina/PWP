from flask_restful import Resource

from src.models.wine import Wine
from src.schemas.schemas import WineSchema

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


class WineList(Resource):
    @classmethod
    def get(cls):
        return {"wines": wine_list_schema.dump(Wine.find_all())}, 200


class WineItem(Resource):
    @classmethod
    def get(cls, name):
        db_wine = Wine.find_by_name(name)
        return wine_schema.dump(db_wine)
