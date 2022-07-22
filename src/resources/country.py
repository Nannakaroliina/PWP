from flask_restful import Resource

from src.models.country import Country
from src.schemas.schemas import CountrySchema

country_schema = CountrySchema()
country_list_schema = CountrySchema(many=True)


class CountryList(Resource):
    @classmethod
    def get(cls):
        return {"countries": country_list_schema.dump(Country.find_all())}, 200


class CountryItem(Resource):
    @classmethod
    def get(cls, name):
        db_country = Country.find_by_name(name)
        return country_schema.dump(db_country)
