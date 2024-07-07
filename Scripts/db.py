from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

db = None

uri = "mongodb+srv://ezhildhiraviya:6x2iLR4Y9j02fT1c@face-recognition.n1qkn6p.mongodb.net/?appName=face-recognition"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['face-db']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


    # face-recognition