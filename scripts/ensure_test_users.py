from pymongo import MongoClient
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/kwik_connect_db')
DB_NAME = os.getenv('DB_NAME', 'kwik_connect_db')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db['users']

users = [
    {
        "email": "test_customer@example.com",
        "password": "Test1234",
        "username": "test_customer",
        "full_name": "Test Customer",
        "role": "customer"
    },
    {
        "email": "test_vendor@example.com",
        "password": "Test1234",
        "username": "test_vendor",
        "full_name": "Test Vendor",
        "role": "vendor"
    },
    {
        "email": "test_courier@example.com",
        "password": "Test1234",
        "username": "test_courier",
        "full_name": "Test Courier",
        "role": "courier"
    }
]

created = []
for u in users:
    existing = users_collection.find_one({'email': u['email']})
    if existing:
        print(f"User exists: {u['email']}")
    else:
        doc = {
            'email': u['email'],
            'username': u['username'],
            'full_name': u['full_name'],
            'role': u['role'],
            'password_hash': generate_password_hash(u['password']),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        users_collection.insert_one(doc)
        print(f"Created user: {u['email']}")
        created.append(u['email'])

print('\nSummary:')
for u in users:
    print(f"- {u['email']}  password: {u['password']}")

if created:
    print('\nCreated users. You can log in using /api/v1/auth/login with the email and password above.')
else:
    print('\nNo users were created; they already exist.')