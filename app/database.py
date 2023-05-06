from decouple import config
from pymongo import MongoClient

db_connection = MongoClient(config("MONGO_CONN"))
db_name = db_connection.TodoDatabase
user_collection = db_name.UserCollection



