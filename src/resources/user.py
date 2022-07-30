from flask import request, jsonify
from flask_jwt_extended import create_access_token, \
    jwt_required, set_access_cookies, \
    unset_jwt_cookies
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from src.schemas.schemas import UserSchema
from src.models.user import User
from src.utils.constants import \
    INVALID_CREDENTIALS, USER_ALREADY_EXISTS, \
    CREATED_SUCCESSFULLY, USER_NOT_FOUND, \
    USER_DELETED, USER_LOGGED_OUT, LOGIN_SUCCESSFUL

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if User.find_by_name(user.username):
            return {"[ERROR]": USER_ALREADY_EXISTS}, 400

        user.password = generate_password_hash(user.password)
        user.add()

        return {"[INFO]": CREATED_SUCCESSFULLY}, 201


class UserItem(Resource):
    @classmethod
    def get(cls, username: str):
        user = User.find_by_name(username)
        if not user:
            return {"[ERROR]": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, username: str):
        user = User.find_by_name(username)
        if not user:
            return {"[ERROR]": USER_NOT_FOUND}, 404

        user.delete()
        return {"[INFO]": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user = request.get_json()
            user_data = user_schema.load(user)
        except ValidationError as e:
            return e.messages, 400

        user = User.find_by_name(user_data.username)

        if not user:
            return {"[ERROR]": USER_NOT_FOUND}, 404

        if user and check_password_hash(user.password, user_data.password):
            response = jsonify({"[INFO]": LOGIN_SUCCESSFUL})
            access_token = create_access_token(identity=user.id)
            set_access_cookies(response, access_token)
            return 'token: ' + access_token, 200

        return {"[ERROR]": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        response = jsonify({"[INFO]": USER_LOGGED_OUT})
        unset_jwt_cookies(response)
        return response, 200
