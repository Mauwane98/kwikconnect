# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-very-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a-super-secret-jwt-key')
    # If DATABASE_URL is not provided, fall back to a local SQLite file for development.
    # DATABASE_URL = os.getenv('DATABASE_URL')
    # if DATABASE_URL:
    #     SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # else:
    #     basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #     sqlite_path = os.path.join(basedir, 'kwikconnect_dev.db')
    #     SQLALCHEMY_DATABASE_URI = f'sqlite:///{sqlite_path}'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB config
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/kwik_connect_db')
    MONGO_DB = os.getenv('DB_NAME', 'kwik_connect_db')

    # Twilio config
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    TWILIO_SMS_NUMBER = os.getenv('TWILIO_SMS_NUMBER')

    WHATSAPP_CONFIG = {
        'account_sid': TWILIO_ACCOUNT_SID,
        'auth_token': TWILIO_AUTH_TOKEN,
        'whatsapp_number': TWILIO_WHATSAPP_NUMBER,
    }

    SMS_CONFIG = {
        'account_sid': TWILIO_ACCOUNT_SID,
        'auth_token': TWILIO_AUTH_TOKEN,
        'sms_number': TWILIO_SMS_NUMBER,
    }
