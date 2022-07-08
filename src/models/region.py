from src.database import db


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)

    # referenced from
    producers = db.relationship("Producer", back_populates="region")
    grapes = db.relationship("Grape", back_populates="region")
    # reference to
    country = db.relationship("Country", back_populates="regions")

    def serialize(self):
        doc = {
            "name": self.name,
            "country": self.country.name
        }

        return doc
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
