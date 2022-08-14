"""
Module for user resource. Provides the methods to get, post and delete
data related to user. Some methods are jwt restricted.
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, \
    jwt_required, set_access_cookies, \
    unset_jwt_cookies
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from src.schemas.schemas import UserSchema
from src.models.user import User
from src.utils.constants import \
    INVALID_CREDENTIALS, USER_ALREADY_EXISTS, \
    CREATED_SUCCESSFULLY, USER_NOT_FOUND, \
    USER_DELETED, USER_LOGGED_OUT, LOGIN_SUCCESSFUL, BAD_REQUEST

user_schema = UserSchema()


class UserRegister(Resource):
    """
    Class that provides a post method to register a user
    """
    @classmethod
    def post(cls):
        """
        Register new user, takes json from request
        and adds new user with hashed password to database.

        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "username": "username",
            "password": "password which is at least 8 char long,
                        contains lower and upper chars, numbers and
                        special character",
            "email": "Optional email",
            "role": "Optional, one of following: developer, producers, expert"
        }

        :return: string info
        """
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if User.find_by_name(user.username):
            return {"[ERROR]": USER_ALREADY_EXISTS}, 409

        user.password = generate_password_hash(user.password)
        user.add()

        return {"[INFO]": CREATED_SUCCESSFULLY}, 201


class UserItem(Resource):
    """
    Class that provides the methods to get user and delete user.
    """
    @classmethod
    def get(cls, username: str):
        """
        Get a user by given username
        :param username: string
        :return: Serialized User object as a JSON
        """
        user = User.find_by_name(username)
        if not user:
            return {"[ERROR]": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    @jwt_required()
    def delete(cls, username: str):
        """
        Delete existing user by given username.
        Headers: Authorization: Bearer access token

        :param username: string
        :return: string info
        """
        user = User.find_by_name(username)
        if not user:
            return {"[ERROR]": USER_NOT_FOUND}, 404

        user.delete()
        return {"[INFO]": USER_DELETED}, 200


class UserLogin(Resource):
    """
    Class provides the post method to login.
    """
    @classmethod
    def post(cls):
        """
        Login an existing user to get JWT access token

        Headers: Authorization: Bearer access token
        Request content-type: Application/JSON
        Request body example, doesn't require all fields:
        {
            "username": "username",
            "password": "password"
        }

        :return: Bearer access token
        """
        try:
            user = request.get_json()
            user_data = user_schema.load(user)
        except ValidationError as e:
            return e.messages, 400

        user = User.find_by_name(user_data.username)

        if user:
            if user and check_password_hash(user.password, user_data.password):
                response = jsonify({"[INFO]": LOGIN_SUCCESSFUL})
                access_token = create_access_token(identity=user.username)
                set_access_cookies(response, access_token)
                return 'Bearer ' + access_token, 200

            return {"[ERROR]": INVALID_CREDENTIALS}, 401
        else:
            return {"[ERROR]": USER_NOT_FOUND}, 404


class UserLogout(Resource):
    """
    Class provides a method to log out the user.
    """
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Log out the currently logged-in user
        Headers: Authorization: Bearer access token

        :return: string info
        """
        try:
            unset_jwt_cookies(jsonify({"[INFO]": USER_LOGGED_OUT}))
            return {"[INFO]": USER_LOGGED_OUT}, 200
        except BadRequest:
            return {"[ERROR]": BAD_REQUEST}, 400
