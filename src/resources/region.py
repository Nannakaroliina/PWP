from flask_restuful import Resource

from src.models.region import Region
from src.schemas.schemas import RegionSchema

region_schema = RegionSchema()
region_list_schema = RegionSchema(many=True)


class RegionList(Resource):
    @classmethod
    def get(cls):
        return {"regions": region_list_schema.dump(Region.find_all())}, 200

    
class RegionItem(Resource):
    @classmethod
    def get(cls, name):
        db_region = Region.find_by_name(name)
        return region_schema.dump(db_region)
