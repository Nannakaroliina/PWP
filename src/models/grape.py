"""
Module that provides database model for Grape with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Grape(db.Model):
    """
    Grape model class for defining the grape
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))
    description = db.Column(db.String(500))

    # referenced from
    wines = db.relationship("Wine", back_populates="grape")
    # reference to
    region = db.relationship("Region", back_populates="grapes")

    def serialize(self):
        """
        Serialize the Grape object to dict
        :return: Grape dict
        """
        doc = {
            "name": self.name,
            "region": self.region.name,
            "description": self.description
        }
        
        return doc
        
    @classmethod
    def find_by_name(cls, name):
        """
        Find the Grape from database by given name
        :param name: string
        :return: Grape
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find the Grape from database by given id
        :param id_: int
        :return: Grape
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Grape"]:
        """
        Find all Grapes from database
        :return: List of Grapes
        """
        return cls.query.all()

    def add(self):
        """
        Add the Grape to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the Grape from database
        """
        db.session.add(self)
        db.session.commit()
