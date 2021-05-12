import os
from datetime import timedelta

import json
from bson.json_util import ObjectId
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from common.db import FLASK_TEST_DB
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import (Home, TokenRefresh, UserLogin, UserLogout,
                            UserRegister)

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.secret_key = os.environ.get(str("SECRET_KEY"))
api = Api(app)

jwt = JWTManager(app)


# This happens when the JWT is created
# When the JWT is created from a request, admin claim is added
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if ObjectId(identity) == ObjectId("60983e917b4a8778497f9733"):
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback(*args, **kwargs):
    return jsonify({
        "message": "The token is expired",
        "error": "expired token"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(reason):
    print(reason)
    return jsonify({"message": "The provided token is invalid"})


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    blocked_jti = FLASK_TEST_DB["block_list"].find_one(
        {"blocklisted_token_id": jwt_payload["jti"]})
    print(blocked_jti)
    return blocked_jti is not None


@jwt.revoked_token_loader
def revoked_token_callback(*args, **kwargs):
    print(*args, **kwargs)
    return jsonify({"message": "The token is revoked"}), 401


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Home, "/")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/token_refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    app.run()
