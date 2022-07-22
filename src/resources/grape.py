from flask_restful import Resource

from src.models.grape import Grape
from src.schemas.schemas import GrapeSchema

grape_schema = GrapeSchema()
grape_list_schema = GrapeSchema(many=True)


class GrapeList(Resource):
    @classmethod
    def get(cls):
        return {"grapes": grape_list_schema.dump(Grape.find_all())}, 200


class GrapeItem(Resource):
    @classmethod
    def get(cls, name):
        db_grape = Grape.find_by_name(name)
        return grape_schema.dump(db_grape)
