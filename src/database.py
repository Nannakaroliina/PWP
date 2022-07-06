from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///winebase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Wine_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)

    wines = db.relationship("Wine", back_populates="wine_type")

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    style = db.Column(db.String(64))
    wine_type_id = db.Column(db.Integer, db.ForeignKey("wine_type.id"))
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    year_produced = db.Column(db.Integer)
    alcohol_percentage = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    picture = db.Column(db.String(128))
    description = db.Column(db.String(500))
    grape_id = db.Column(db.Integer, db.ForeignKey("grape.id"))

    wine_type = db.relationship("Wine_type", back_populates="wines")
    producer = db.relationship("Producer", back_populates="wines")
    grape = db.relationship("Grape", back_populates="wines")

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=False)
    description = db.Column(db.String(500))

    #referenced from
    wines = db.relationship("Wine", back_populates="producer")
    #reference to
    region = db.relationship("Region", back_populates="producers")

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)

    #referenced from
    producers = db.relationship("Producer", back_populates="region")
    grapes = db.relationship("Grape", back_populates="region")
    #reference to
    country = db.relationship("Country", back_populates="regions")

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    regions = db.relationship("Region", back_populates="country")

class Grape(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=False)
    description = db.Column(db.String(500))
    
    #referenced from
    wines = db.relationship("Wine", back_populates="grape")
    #reference to
    region = db.relationship("Region", back_populates="grapes")