"""
Order Channel Model

This model handles different ordering channels (WhatsApp, SMS, phone calls, app)
and their specific requirements.
"""


from bson.objectid import ObjectId
from flask import current_app

import enum
from .base_model import BaseModel


class OrderChannelType(enum.Enum):
    """
    Supported ordering channels
    """
    APP = 'app'
    WHATSAPP = 'whatsapp'
    SMS = 'sms'
    PHONE = 'phone'
    USSD = 'ussd'  # For feature phones
    WEB = 'web'    # Web browser orders

class OrderChannel(BaseModel):
    """
    Stores information about different ordering channels and their configurations
    """
    collection_name = 'order_channels'
    

    
    def __init__(self, channel_type, is_active=True, config=None, phone_number=None,
                 api_credentials=None, webhook_url=None, rate_limit=None,
                 operating_hours=None, error_messages=None, success_messages=None,
                 menu_format=None, _id=None):
        self.channel_type = channel_type
        self.is_active = is_active
        self.config = config
        self.phone_number = phone_number
        self.api_credentials = api_credentials
        self.webhook_url = webhook_url
        self.rate_limit = rate_limit
        self.operating_hours = operating_hours
        self.error_messages = error_messages
        self.success_messages = success_messages
        self.menu_format = menu_format
        self._id = _id if _id else ObjectId()

    def save(self):
        channel_data = {
            'channel_type': self.channel_type.value,
            'is_active': self.is_active,
            'config': self.config,
            'phone_number': self.phone_number,
            'api_credentials': self.api_credentials,
            'webhook_url': self.webhook_url,
            'rate_limit': self.rate_limit,
            'operating_hours': self.operating_hours,
            'error_messages': self.error_messages,
            'success_messages': self.success_messages,
            'menu_format': self.menu_format
        }
        coll = self.get_collection()
        if self._id:
            coll.update_one({'_id': self._id}, {'$set': channel_data}, upsert=True)
        else:
            result = coll.insert_one(channel_data)
            self._id = result.inserted_id
        return self

    @staticmethod
    def find_by_id(channel_id):
        return OrderChannel.find_by_id(channel_id)

    @staticmethod
    def get_channel_config(channel_type):
        coll = OrderChannel.get_collection()
        channel_data = coll.find_one({
            'channel_type': channel_type.value,
            'is_active': True
        })
        if channel_data:
            return channel_data.get('config')
        return None

    def to_dict(self):
        return {
            'id': str(self._id),
            'channel_type': self.channel_type.value,
            'is_active': self.is_active,
            'config': self.config,
            'phone_number': self.phone_number,
            'api_credentials': self.api_credentials,
            'webhook_url': self.webhook_url,
            'rate_limit': self.rate_limit,
            'operating_hours': self.operating_hours,
            'error_messages': self.error_messages,
            'success_messages': self.success_messages,
            'menu_format': self.menu_format
        }

    def __repr__(self):
        return f'<OrderChannel {self.channel_type.value}>'