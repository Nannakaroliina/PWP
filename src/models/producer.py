"""
Module that provides database model for Producer with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class Producer(db.Model):
    """
    Producer model class for defining the producer
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))
    description = db.Column(db.String(500))

    # referenced from
    wines = db.relationship("Wine", back_populates="producer")
    # reference to
    region = db.relationship("Region", back_populates="producers")

    def serialize(self):
        """
        Serialize the Producer object to dict
        :return: Producer dict
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
        Find the Producer from database by given name
        :param name: string
        :return: Producer
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        Find the Producer from database by given id
        :param id_: int
        :return: Producer
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["Producer"]:
        """
        Find all the Producers from database
        :return: List of Producers
        """
        return cls.query.all()

    def add(self):
        """
        Add the Producer to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the Producer from database
        """
        db.session.add(self)
        db.session.commit()
