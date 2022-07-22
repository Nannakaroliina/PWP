from flask_restful import Resource

from src.models.wine_type import Wine_type
from src.schemas.schemas import WineTypeSchema

wine_type_schema = WineTypeSchema()
wine_type_list_schema = WineTypeSchema(many=True)


class Wine_typeList(Resource):
    @classmethod
    def get(cls):
        return {"wine_types": wine_type_list_schema.dump(Wine_type.find_all())}, 200


class Wine_typeItem(Resource):
    @classmethod
    def get(cls, name):
        db_wine_type = Wine_type.find_by_type(name)
        return wine_type_schema.dump(db_wine_type)
