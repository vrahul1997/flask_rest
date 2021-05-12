import json

from bson.json_util import ObjectId, dumps
from common.db import FLASK_TEST_DB
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required, get_jwt)
from flask_restful import Resource, reqparse

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                          type=str,
                          required=True,
                          help="Username field is required")
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="Password field is required")


class Home(Resource):
    def get(self):
        return "This is Home"


class UserModel:
    def __init__(self, _id=None, username=None, password=None):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        user_collection = FLASK_TEST_DB["users"]
        result = json.loads(
            dumps(user_collection.find_one({"username": username})))
        if result:
            result["_id"] = result["_id"]["$oid"]
            user = self(**result)
            return user
        else:
            return None

    @classmethod
    def find_by_id(self, _id):
        user_collection = FLASK_TEST_DB["users"]
        result = json.loads(
            dumps(user_collection.find_one({"_id": ObjectId(_id)})))
        if result:
            result["_id"] = result["_id"]["$oid"]
            user = self(**result)
            return user
        else:
            return None


class UserRegister(Resource):
    @classmethod
    def post(self):
        data = _user_parser.parse_args()  #error first approach

        user = UserModel.find_by_username(data["username"])
        if user is not None:
            print(user)
            return {
                "message":
                f"A user with username {data['username']} is already created"
            }

        user_collection = FLASK_TEST_DB["users"]
        user_collection.insert_one({
            "username": data["username"],
            "password": data["password"]
        })

        return {"message": "User created successfully"}, 201


class UserLogin(Resource):
    @classmethod
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and user.password == data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "unauthorized"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blocklist_collection = FLASK_TEST_DB["block_list"]
        blocklist_collection.insert_one({"blocklisted_token_id": jti})
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": new_token}, 200
