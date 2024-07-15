from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv(".dev.env")

db = None

db_url = os.getenv("MONGODB_URI")
print("string: ", db_url)

client = MongoClient(db_url, server_api=ServerApi('1'))

db = client['face-db']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
