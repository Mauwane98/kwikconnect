from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_mongo_connection():
    load_dotenv()
    
    # Get MongoDB URI from environment
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/kwik_connect_db')
    db_name = os.getenv('DB_NAME', 'kwik_connect_db')
    
    try:
        # Create MongoDB client
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        # Test connection
        db.command('ping')
        print(f"Successfully connected to MongoDB database: {db_name}")
        print(f"MongoDB URI: {mongo_uri}")
        
        # List collections
        collections = db.list_collection_names()
        print("\nAvailable collections:")
        for collection in collections:
            print(f"- {collection}")
            
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return False

if __name__ == '__main__':
    test_mongo_connection()