from typing import List

from src.database import db


class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))
    description = db.Column(db.String(500))

    # referenced from
    wines = db.relationship("Wine", back_populates="producer")
    # reference to
    region = db.relationship("Region", back_populates="producers")

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
    def find_all(cls) -> List["Producer"]:
        return cls.query.all()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()
