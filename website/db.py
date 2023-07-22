import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import certifi
from gridfs import GridFS

# Initialize the MongoDB client and GridFS
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://admin:{password}@database.lrh5cyk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client.get_database('test')
fs = GridFS(db)