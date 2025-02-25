"""
Module that provides database model for Wine with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Wine(db.Model):
    """
    Wine model class for defining the wine
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    style = db.Column(db.String(64))
    wine_type_id = db.Column(db.Integer, db.ForeignKey("wine_type.id"))
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    year_produced = db.Column(db.Integer)
    alcohol_percentage = db.Column(db.Float(precision=2))
    volume = db.Column(db.Integer)
    picture = db.Column(db.String(500))
    description = db.Column(db.String(500))
    grape_id = db.Column(db.Integer, db.ForeignKey("grape.id"))

    wine_type = db.relationship("Wine_type", back_populates="wines")
    producer = db.relationship("Producer", back_populates="wines")
    grape = db.relationship("Grape", back_populates="wines")

    def serialize(self):
        """
        Serialize the wine object to dict
        :return: Wine dict
        """
        doc = {
            "name": self.name,
            "wine_type": self.wine_type.type,
            "style": self.style,
            "description": self.description,
            "grape": self.grape.name,
            "producer": self.producer.name,
            "year_produced": self.year_produced,
            "alcohol_percentage": self.alcohol_percentage,
            "volume": self.volume,
            "picture": self.picture
        }

        return doc

    @classmethod
    def find_by_name(cls, name):
        """
        Find wine from database by given name
        :param name: string
        :return: Wine
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find wine from database by given id
        :param id_: int
        :return: Wine
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Wine"]:
        """
        Find all wines from database
        :return: List of Wines
        """
        return cls.query.all()

    def add(self):
        """
        Add Wine to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete Wine from database
        """
        db.session.delete(self)
        db.session.commit()
