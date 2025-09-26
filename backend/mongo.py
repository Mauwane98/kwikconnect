# mongo.py

from pymongo import MongoClient
from backend.config.config import Config
import os
from flask import current_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Get MongoDB connection from configuration"""
    try:
        # Get MongoDB URI from environment or config
        if current_app:
            mongo_uri = current_app.config['MONGO_URI']
            db_name = current_app.config.get('MONGO_DB', 'kwik_connect_db')
        else:
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/kwik_connect_db')
            db_name = os.getenv('DB_NAME', 'kwik_connect_db')
        
        # Create MongoDB client
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        # Test connection
        db.command('ping')
        print(f"Successfully connected to MongoDB database: {db_name}")
        
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        raise
