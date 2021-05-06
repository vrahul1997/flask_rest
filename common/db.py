from pymongo import MongoClient
import os

# client = MongoClient(os.environ.get("MONGO_CLIENT"))
client = MongoClient(
    "mongodb+srv://rahulll:Ra_Pun_zel@2002@cluster0.ucpg9.mongodb.net/flask_test?retryWrites=true&w=majority"
)
FLASK_TEST_DB = client["flask_test"]