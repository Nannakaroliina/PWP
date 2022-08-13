"""
Module that provides database model for User with
methods to add or modify the data on database
"""
from typing import List

from src.database import db


class User(db.Model):
    """
    User model class for defining the user
    database model and methods.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    role = db.Column(db.String(32))

    @classmethod
    def find_by_name(cls, username):
        """
        Find the user from database by given username
        :param username: string
        :return: User
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id_):
        """
        find the user from database by given id
        :param id_: int
        :return: Wine
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List["User"]:
        """
        Find all users from database
        :return: List of Users
        """
        return cls.query.all()

    def add(self):
        """
        Add User to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete User from database
        """
        db.session.add(self)
        db.session.commit()
