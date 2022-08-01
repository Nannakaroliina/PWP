import os
import tempfile
import pytest as pytest

from flask import Flask
from src.app import app
from src.database import db


def _populate_db():
    # TODO add db population for api testing
    pass
    # db.session.add()
    # db.session.commit()


@pytest.fixture
def client():
    """Configures the app for testing

    :return: App for testing
    """
    app.app_context().push()
    app.config["TESTING"] = True
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
