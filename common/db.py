from pymongo import MongoClient
import os

# client = MongoClient(os.environ.get("MONGO_CLIENT"))
client = MongoClient(
    "mongodb+srv://rahulll:N20FBJ7BHPAorXS8@cluster0.ucpg9.mongodb.net/test?authSource=admin&replicaSet=atlas-11wr07-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
)
FLASK_TEST_DB = client["flask_test"]