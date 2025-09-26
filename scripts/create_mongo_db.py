# Script to create a MongoDB database and collection so it appears in MongoDB Compass
from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient('mongodb://localhost:27017')

# Use the database name from your .env
DB_NAME = 'kwik_connect_db'
db = client[DB_NAME]

# Create a collection and insert a test document
collection = db['test_collection']
collection.insert_one({'msg': 'Hello, MongoDB!'})

print(f"Database '{DB_NAME}' and collection 'test_collection' created with a test document.")
