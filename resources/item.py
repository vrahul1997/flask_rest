import json

from bson.json_util import ObjectId, dumps
from common.db import FLASK_TEST_DB
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

items_collection = FLASK_TEST_DB["items"]


class ItemModel:
    def __init__(self, _id, store_id, name, price):
        self._id = _id
        self.store_id = store_id
        self.name = name
        self.price = price

    @classmethod
    def find_by_name(self, name):
        result = items_collection.find_one({"name": name})
        result = json.loads(dumps(result))
        if result:
            result["_id"] = result["_id"]["$oid"]
            item = self(**result)
            return item
        else:
            return None


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="price field is required")
    parser.add_argument("store_id",
                        type=str,
                        required=True,
                        help="store_id field is required")

    @jwt_required()
    def get(self, name):
        result = items_collection.find_one({"name": name})
        if result is None:
            return {"message": "No such item found"}, 400
        else:
            item = json.loads(dumps(result))
            return {"item": item}, 200

    @jwt_required()
    def post(self, name):
        result = items_collection.find_one({"name": name})
        if result is None:
            data = Item.parser.parse_args(
            )  # placed here to maintain error first approach
            print(data)
            item = {
                "store_id": ObjectId(data["store_id"]),
                "name": name,
                "price": data["price"]
            }
            items_collection.insert_one(item)
            return (
                {
                    "item": json.loads(dumps(item))
                }, 201
            )  # 201 is for something created, 202 for the creation of item is accepted
        else:
            return {"message": f"An item with {name} already exists"}

    @jwt_required()
    def delete(self, name):
        if items_collection.find_one({"name": name}):
            items_collection.delete_one({"name": name})
            return {
                "message": "Item is deleted succesfully"
            }, 200  #resourse deleted succesfully
        else:
            return {
                "message":
                f"This requested item to be deleted with name:'{name}' is not present"
            }, 400

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        result = items_collection.find_one({"name": name})
        item = {
            "name": name,
            "price": data["price"],
            "store_id": ObjectId(data["store_id"])
        }
        if result is None:
            items_collection.insert_one(item)
        else:
            items_collection.update_one({"name": name}, {
                "$set": {
                    "price": data["price"],
                    "store_id": ObjectId(data["store_id"])
                }
            })
        return {
            "item": json.loads(dumps(items_collection.find_one({"name":
                                                                name})))
        }, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        result = items_collection.find()
        items = json.loads(dumps(result))
        return {"items": items}, 200 if items else 404  #not found
