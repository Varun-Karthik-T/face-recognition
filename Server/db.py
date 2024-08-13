from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from models import *

load_dotenv(".dev.env")

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

existing_collections = db.list_collection_names()

for collection_name, validator in collections_to_create.items():
    if collection_name not in existing_collections:
        db.create_collection(collection_name, validator=validator)

test_documents = {
    "Users": {"name": "Test User", "email": "test@example.com"},
    "History": {"user_id": "12345", "action": "login", "timestamp": "2023-01-01T00:00:00Z"},
    "Profiles": {"user_id": "12345", "profile_data": {"age": 30, "gender": "male"}},
    "Notifications": {"user_id": "12345", "message": "Welcome!", "timestamp": "2023-01-01T00:00:00Z"}
}

for collection_name, document in test_documents.items():
    try:
        db[collection_name].insert_one(document)
        print(f"Inserted test document into {collection_name} collection successfully.")
    except Exception as e:
        print(f"Failed to insert test document into {collection_name} collection: {e}")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
