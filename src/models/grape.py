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
