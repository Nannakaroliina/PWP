"""
Module that provides database model for Region with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Region(db.Model):
    """
    Region model class for defining the region
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))

    # referenced from
    producers = db.relationship("Producer", back_populates="region")
    grapes = db.relationship("Grape", back_populates="region")
    # reference to
    country = db.relationship("Country", back_populates="regions")

    def serialize(self):
        """
        Serialize the Region object to dict
        :return: Region dict
        """
        doc = {
            "name": self.name,
            "country": self.country.name
        }

        return doc
    
    @classmethod
    def find_by_name(cls, name):
        """
        Find the region from database by given name
        :param name: string
        :return: Region
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find the region from database by given id
        :param id_: int
        :return: Region
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Region"]:
        """
        Find all regions from database
        :return: List of Regions
        """
        return cls.query.all()

    def add(self):
        """
        Add Region to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete Region from database
        """
        db.session.delete(self)
        db.session.commit()
