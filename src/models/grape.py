from typing import List

from src.database import db


class Grape(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=False)
    description = db.Column(db.String(500))

    # referenced from
    wines = db.relationship("Wine", back_populates="grape")
    # reference to
    region = db.relationship("Region", back_populates="grapes")

    def serialize(self):
        doc = {
            "name": self.name,
            "region": self.region.name,
            "description": self.description
        }
        
        return doc
        
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["Grape"]:
        return cls.query.all()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()
