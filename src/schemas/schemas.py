"""
Module that contains the schemas for validating the data.
"""
from datetime import date

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
current_date = date.today()


class UserSchema(Schema):
    """
    User schema which validates the user fields. Contains some regex validation for
    email and password. Returns user object on load method. Password is load only,
    so it will not be available through dump.
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(max=128))
    password = fields.Str(load_only=True, validate=password_regex, required=True)
    email = fields.Str(validate=email_regex)
    role = fields.Str(validate=OneOf(['developer', 'producer', 'expert']))

    @post_load
    def make_user(self, data, **kwargs):
        """
        Make user object when loading through user schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: User object
        """
        return User(**data)


class WineSchema(Schema):
    """
    Wine schema which validates the wine fields. Uses nested schemas for
    producer, wine type and grape where it provides name or type only.
    Production year restriction is based on oldest known wine and current year.
    Volume defaults to most common when missing.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    style = fields.Str(validate=Length(max=128))
    wine_type = fields.Nested(lambda: WineTypeSchema(only=('type',)))
    producer = fields.Nested(lambda: ProducerSchema(only=('name',)))
    year_produced = fields.Int(validate=Range(min=1867, max=current_date.year))
    alcohol_percentage = fields.Float(metadata={"precision": 2})
    volume = fields.Int(validate=Range(min=187, max=1500), load_default=750)
    picture = fields.Str(validate=Length(max=500))
    description = fields.Str(validate=Length(max=500))
    grape = fields.Nested(lambda: GrapeSchema(only=('name',)))

    @post_load
    def make_wine(self, data, **kwargs):
        """
        Make wine object when loading through wine schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Wine object
        """
        return Wine(**data)


class WineTypeSchema(Schema):
    """
    Wine type schema which validates the wine type fields.
    Nested schema for wines excludes the wine_type to avoid loops.
    """
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True, validate=Length(max=64))
    wines = fields.List(fields.Nested(WineSchema(exclude=('wine_type',))))

    @post_load
    def make_wine_type(self, data, **kwargs):
        """
        Make wine type object when loading through wine type schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Wine type object
        """
        return Wine_type(**data)


class ProducerSchema(Schema):
    """
    Producer schema which validates the producer fields.
    Nested schema for region contains only name and
    wines excludes the wine_type to avoid loops.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('producer',))))

    @post_load
    def make_producer(self, data, **kwargs):
        """
        Make producer object when loading through producer schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Producer object
        """
        return Producer(**data)


class CountrySchema(Schema):
    """
    Country schema which validates the country fields.
    Nested schema for regions excludes the country to avoid loops.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    regions = fields.List(fields.Nested(lambda: RegionSchema(exclude=('country',))))

    @post_load
    def make_country(self, data, **kwargs):
        """
        Make country object when loading through country schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Country object
        """
        return Country(**data)


class GrapeSchema(Schema):
    """
    Grape schema which validates the grape fields.
    Nested schema for region contains only name and
    wines excludes the grape to avoid loops.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=64))
    region = fields.Nested(lambda: RegionSchema(only=('name',)))
    description = fields.Str(validate=Length(max=500))
    wines = fields.List(fields.Nested(WineSchema(exclude=('grape',))))

    @post_load
    def make_grape(self, data, **kwargs):
        """
        Make grape object when loading through grape schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Grape object
        """
        return Grape(**data)


class RegionSchema(Schema):
    """
    Region schema which validates the region fields.
    Nested schema for country contains only name, and
    producers and grapes excludes the region to avoid loops.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=128))
    country = fields.Nested(CountrySchema(only=('name',)))
    producers = fields.List(fields.Nested(ProducerSchema(exclude=('region',))))
    grapes = fields.List(fields.Nested(GrapeSchema(exclude=('region',))))

    @post_load
    def make_region(self, data, **kwargs):
        """
        Make region object when loading through region schema
        :param data: input data
        :param kwargs: not used but must be included
        :return: Region object
        """
        return Region(**data)
