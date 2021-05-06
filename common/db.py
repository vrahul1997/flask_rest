from pymongo import MongoClient
import os

# client = MongoClient(os.environ.get("MONGO_CLIENT"))
client = MongoClient(
    "mongodb+srv://rahulll:N20FBJ7BHPAorXS8@cluster0.ucpg9.mongodb.net/flask_test?retryWrites=true&w=majority"
)

FLASK_TEST_DB = client["flask_test"]