from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from models import *

load_dotenv(".env")

db = None

db_url = os.getenv("MONGODB_URI")
client = MongoClient(db_url, server_api=ServerApi('1'))

db = client['face-db']

collections_to_create = {
    "Users": user_schema,
    "History": history_schema,
    "Profiles": profiles_schema,
    "Notifications": notifications_schema
}

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
existing_collections = db.list_collection_names()

for collection_name, validator in collections_to_create.items():
    if collection_name not in existing_collections:
        db.create_collection(collection_name, validator=validator)

