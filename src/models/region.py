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
