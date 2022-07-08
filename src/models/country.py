from src.database import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    regions = db.relationship("Region", back_populates="country")
