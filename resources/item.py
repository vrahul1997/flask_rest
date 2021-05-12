import json

from bson.json_util import ObjectId, dumps
from common.db import FLASK_TEST_DB
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse

from .store import StoreModel

items_collection = FLASK_TEST_DB["items"]
stores_collection = FLASK_TEST_DB["stores"]


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

    @jwt_required(fresh=True)
    def post(self, name):
        result = items_collection.find_one({"name": name})
        if result is None:
            data = Item.parser.parse_args(
            )  # placed here to maintain error first approach
            print(data)
            try:
                item = {
                    "store_id": ObjectId(data["store_id"]),
                    "name": name,
                    "price": data["price"]
                }
            except Exception:
                return {"message": "ObjectId entered is wrong"}
            if StoreModel.find_by_id(item["store_id"]) is None:
                return {"message": "No store found"}, 404
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
        claims = get_jwt()  #to get the claims in the JWT
        if not claims["is_admin"]:
            return {"message": "Admin previlege is required"}, 401
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
        try:
            item = {
                "store_id": ObjectId(data["store_id"]),
                "name": name,
                "price": data["price"]
            }
        except Exception:
            return {"message": "ObjectId entered is wrong"}
        if result is None:
            if StoreModel.find_by_id(item["store_id"]) is None:
                return {"message": "No store found"}, 404
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
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        result = items_collection.find()
        if user_id:
            items = json.loads(dumps(result))
            return {"items": items}, 200
        return {
            "items": [names["name"] for names in json.loads(dumps(result))],
            "message": "More data will be provided if you are logged in"
        }
