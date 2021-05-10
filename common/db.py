from pymongo import MongoClient
import os

# client = MongoClient(os.environ.get("MONGO_CLIENT"))
password = os.environ.get("MONGO_PASSWORD")
client = MongoClient(
    f"mongodb+srv://rahulll:{password}@cluster0.ucpg9.mongodb.net/flask_test?retryWrites=true&w=majority"
)

FLASK_TEST_DB = client["flask_test"]