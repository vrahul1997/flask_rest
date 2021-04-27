import json

from bson.json_util import ObjectId, dumps
from common.db import FLASK_TEST_DB
from flask_restful import Resource, reqparse


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
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Username field is required")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Password field is required")

    def post(self):
        data = UserRegister.parser.parse_args()  #error first approach

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
