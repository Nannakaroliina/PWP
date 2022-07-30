from marshmallow import fields, Schema, post_load
from marshmallow.validate import Regexp, Length, Range, OneOf

from src.models.country import Country
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.region import Region
from src.models.user import User
from src.models.wine import Wine
from src.models.wine_type import Wine_type

email_regex = Regexp(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_regex = Regexp(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(max=128))
    password = fields.Str(load_only=True, validate=password_regex, required=True)
    email = fields.Str(validate=email_regex)
    role = fields.Str(validate=OneOf(['developer', 'producer', 'expert']))

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class WineSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    style = fields.Str(validate=Length(max=128))
    wine_type = fields.Nested(lambda: WineTypeSchema(only=('type',)))
    producer = fields.Nested(lambda: ProducerSchema(only=('name',)))
    # production year min is based on oldest known wine
    year_produced = fields.Int(validate=Range(min=1867, max=2022))
    alcohol_percentage = fields.Float(precision=2)
    volume = fields.Int(validate=Range(min=187, max=1500), missing=750)
    # could add the url regex but then again, picture might not always be available
    picture = fields.Str(validate=Length(max=500))
    description = fields.Str(validate=Length(max=500))
    grape = fields.Nested(lambda: GrapeSchema(only=('name',)))

    @post_load
    def make_wine(self, data, **kwargs):
        return Wine(**data)


class WineTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True, validate=Length(max=64))
    wines = fields.List(fields.Nested(WineSchema(exclude=('wine_type',))))

    @post_load
    def make_wine_type(self, data, **kwargs):
        return Wine_type(**data)


class ProducerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('producer',))))

    @post_load
    def make_producer(self, data, **kwargs):
        return Producer(**data)


class CountrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    regions = fields.List(fields.Nested(lambda: RegionSchema(exclude=('country',))))

    @post_load
    def make_country(self, data, **kwargs):
        return Country(**data)


class GrapeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('grape',))))

    @post_load
    def make_grape(self, data, **kwargs):
        return Grape(**data)


class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    country = fields.Nested(CountrySchema(only=('name',)))
    producers = fields.List(fields.Nested(ProducerSchema(exclude=('region',))))
    grapes = fields.List(fields.Nested(GrapeSchema(exclude=('region',))))

    @post_load
    def make_region(self, data, **kwargs):
        return Region(**data)