"""
Module that provides database model for Country with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Country(db.Model):
    """
    Country model class for defining the country
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    regions = db.relationship("Region", back_populates="country")

    def serialize(self):
        """
        Serialize the Country object to dict
        :return: Country dict
        """
        doc = {
            "name": self.name
        }
        
        return doc
            
    @classmethod
    def find_by_name(cls, name):
        """
        Find the Country from database by given name
        :param name: string
        :return: Country
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find the Country from database by given id
        :param id_: int
        :return: Country
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Country"]:
        """
        Find all Countries from database
        :return: List of Countries
        """
        return cls.query.all()

    def add(self):
        """
        Add the Country to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the Country from database
        """
        db.session.add(self)
        db.session.commit()
