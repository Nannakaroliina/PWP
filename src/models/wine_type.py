"""
Module that provides database model for Wine type with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Wine_type(db.Model):
    """
    Wine type model class for defining the wine type
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)

    wines = db.relationship("Wine", back_populates="wine_type")

    def serialize(self):
        """
        Serialize the wine type object to dict
        :return: Wine type dict
        """
        doc = {
            "type": self.type
        }

        return doc

    @classmethod
    def find_by_type(cls, type_):
        """
        Find the wine type from database by given type
        :param type_: string
        :return: Wine type
        """
        return cls.query.filter_by(type=type_).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find the wine type from database by given id
        :param id_: int
        :return: Wine type
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Wine_type"]:
        """
        Find all wine types from database
        :return: List of Wine types
        """
        return cls.query.all()
    
    def add(self):
        """
        Add the Wine type to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the Wine type from database
        """
        db.session.delete(self)
        db.session.commit()
