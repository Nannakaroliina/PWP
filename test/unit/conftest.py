import os
import tempfile
import pytest as pytest

from flask import Flask
from werkzeug.security import generate_password_hash

from src.app import app
from src.database import db
from src.models.country import Country
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.region import Region
from src.models.user import User
from src.models.wine import Wine
from src.models.wine_type import Wine_type


def _populate_db():
    password = generate_password_hash("Test-password1234")
    for i in range(1, 4):
        wine_type = Wine_type(type='test type {}'.format(i))
        db.session.add(wine_type)

        country = Country(name='test country {}'.format(i))
        db.session.add(country)

        region = Region(name='test region {}'.format(i))
        region.country = country
        db.session.add(region)

        grape = Grape(
            name='test grape {}'.format(i),
            description='test description'
        )
        grape.region = region
        db.session.add(grape)

        producer = Producer(
            name='test producer {}'.format(i),
            description='test description'
        )
        producer.region = region
        db.session.add(producer)

        wine = Wine(
            name="test wine {}".format(i),
            year_produced=2022,
            alcohol_percentage=20,
            volume=750,
            picture='test picture',
            description='test description',
            style='test style'
        )
        wine.wine_type = wine_type
        wine.producer = producer
        wine.grape = grape
        db.session.add(wine)

        user = User(
            username="test user {}".format(i),
            password=password,
            email="testi@email.com",
            role="developer"
        )
        db.session.add(user)
    db.session.commit()


@pytest.fixture
def client():
    """Configures the app for testing

    :return: App for testing
    """
    app.app_context().push()
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    app.config["JWT_SECRET_KEY"] = "testing"
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    db.create_all()
    _populate_db()

    yield app.test_client()

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


@pytest.fixture()
def db_handle():
    """Configures the database for testing

    :return: Database for testing
    """
    app = Flask(__name__)
    app.app_context().push()
    app.config["TESTING"] = True
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield db

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
