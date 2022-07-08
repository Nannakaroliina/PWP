from src.database import db


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    style = db.Column(db.String(64))
    wine_type_id = db.Column(db.Integer, db.ForeignKey("wine_type.id"))
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    year_produced = db.Column(db.Integer)
    alcohol_percentage = db.Column(db.Float(precision=2))
    volume = db.Column(db.Integer)
    picture = db.Column(db.String(128))
    description = db.Column(db.String(500))
    grape_id = db.Column(db.Integer, db.ForeignKey("grape.id"))

    wine_type = db.relationship("Wine_type", back_populates="wines")
    producer = db.relationship("Producer", back_populates="wines")
    grape = db.relationship("Grape", back_populates="wines")
