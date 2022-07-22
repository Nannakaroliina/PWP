from marshmallow import fields, Schema
from marshmallow.validate import Regexp, Length, Range

email_regex = Regexp(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_regex = Regexp(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(max=128))
    password = fields.Str(load_only=True, validate=Length(min=8, max=128), required=True)
    email = fields.Str(validate=email_regex, required=True)
    role = fields.Str(required=True, validate=Length(max=32))


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


class WineTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True, validate=Length(max=64))
    wines = fields.List(fields.Nested(WineSchema(exclude=('wine_type',))))


class ProducerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('producer',))))


class CountrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    regions = fields.List(fields.Nested(lambda: RegionSchema(exclude=('country',))))


class GrapeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('grape',))))


class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    country = fields.Nested(CountrySchema(only=('name',)))
    producers = fields.List(fields.Nested(ProducerSchema(exclude=('region',))))
    grapes = fields.List(fields.Nested(GrapeSchema(exclude=('region',))))