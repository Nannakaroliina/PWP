from sqlite3 import IntegrityError

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.models.country import Country
from src.schemas.schemas import CountrySchema
from src.utils.constants import ALREADY_EXISTS, ERROR_DELETING, ERROR_INSTERTING, NOT_JSON

country_schema = CountrySchema()
country_list_schema = CountrySchema(many=True)


class CountryList(Resource):

    @classmethod
    def get(cls):
        return {"countries": country_list_schema.dump(Country.find_all())}, 200

    @classmethod
    @jwt_required()
    def post(cls):

        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 500

        content = request.get_json()

        try:
            country = country_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        if Country.find_by_name(content["name"]):
            return {"[ERROR]": ALREADY_EXISTS}, 409

        try:
            country.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSTERTING}, 500

        return country_schema.dump(country), 201


class CountryItem(Resource):

    @classmethod
    def get(cls, name):
        db_country = Country.find_by_name(name)
        return country_schema.dump(db_country)

    @classmethod
    @jwt_required()
    def delete(cls, name):

        item = Country.find_by_name(name)

        if item:
            try:
                item.delete()
                return {"message": "{} deleted".format(item.name)}, 200
            except:
                return {"[ERROR]": ERROR_DELETING}, 500

        return {"[ERROR]": "Country {} not found".format(name)}, 404

    @classmethod
    @jwt_required()
    def put(cls, name):

        if not request.is_json:
            return {"[ERROR]": NOT_JSON}, 415

        content = request.get_json()

        item = Country.find_by_name(name)

        if item:
            item.name = content["name"]
        else:
            return {"[ERROR]": "Country not found"}, 404

        try:
            item = country_schema.load(content)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.add()
        except IntegrityError:
            return {"[ERROR]": ERROR_INSTERTING}, 500

        return country_schema.dump(item), 200