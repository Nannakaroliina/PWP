from src.database import db


class Wine_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)

    wines = db.relationship("Wine", back_populates="wine_type")
