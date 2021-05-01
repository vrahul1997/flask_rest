from pymongo import MongoClient
import os

client = MongoClient(os.environ.get("MONGO_CLIENT"))
FLASK_TEST_DB = client["flask_test"]