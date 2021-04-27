from pymongo import MongoClient
from flask import current_app, g
import os
from flask.cli import with_appcontext

client = MongoClient(os.environ.get("MONGO_CLIENT"))
FLASK_TEST_DB = client["flask_test"]