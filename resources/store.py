import json

from bson.json_util import dumps, ObjectId
from common.db import FLASK_TEST_DB
from flask_jwt_extended import jwt_required
from flask_restful import Resource

stores_collection = FLASK_TEST_DB["stores"]


class StoreModel:
    def __init__(self, _id, name):
        self._id = _id
        self._name = name

    @classmethod
    def find_by_name(self, name):
        store_collection = FLASK_TEST_DB["stores"]
        result = json.loads(dumps(store_collection.find_one({"name": name})))
        if result:
            result["_id"] = result["_id"]["$oid"]
            store = self(**result)
            return store
        else:
            return None

    @classmethod
    def find_by_id(self, _id):
        stores_collection = FLASK_TEST_DB["stores"]
        result = json.loads(dumps(stores_collection.find_one({"_id": _id})))
        if result:
            result["_id"] = result["_id"]["$oid"]
            store = self(**result)
            return store
        else:
            return None


class Store(Resource):
    @jwt_required()
    def get(self, name):
        result = stores_collection.find_one({"name": name})
        if result is None:
            return {"message": "No such store found"}, 400
        else:
            store = json.loads(dumps(result))
            return {"store": store}, 200

    @jwt_required()
    def post(self, name):
        result = stores_collection.find_one({"name": name})
        if result is None:
            store = {"name": name}
            stores_collection.insert_one(store)
            return {"store": json.loads(dumps(store))}, 201
        else:
            return {"message": f"Store with {name} already exists"}

    @jwt_required()
    def delete(self, name):
        if stores_collection.find_one({"name": name}):
            stores_collection.delete_one({"name": name})
            return {
                "message": f"Store: {name} is deleted succesfully"
            }, 200  #resourse deleted succesfully
        else:
            return {
                "message":
                f"This requested store to be deleted with name:'{name}' is not present"
            }, 400


class StoreList(Resource):
    @jwt_required()
    def get(self):
        result = stores_collection.find()
        stores = json.loads(dumps(result))
        return {"stores": stores}, 200 if stores else 404  #not found
