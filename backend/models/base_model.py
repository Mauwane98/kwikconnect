

from datetime import datetime
from bson import ObjectId
from flask import current_app

class BaseModel:
    """Base class for all models, providing common database operations."""
    
    collection_name = None  # Must be set by child classes
    
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for this model."""
        if not cls.collection_name:
            raise ValueError(f"collection_name not set for model {cls.__name__}")
        return current_app.mongo_db[cls.collection_name]
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new document in the collection."""
        kwargs['created_at'] = datetime.utcnow()
        kwargs['updated_at'] = datetime.utcnow()
        result = cls.get_collection().insert_one(kwargs)
        kwargs['_id'] = result.inserted_id
        return kwargs
    
    @classmethod
    def find_one(cls, query):
        """Find a single document matching the query."""
        return cls.get_collection().find_one(query)
    
    @classmethod
    def find_by_id(cls, id):
        """Find a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.get_collection().find_one({'_id': id})
    
    @classmethod
    def find(cls, query=None):
        """Find all documents matching the query."""
        return list(cls.get_collection().find(query or {}))
    
    @classmethod
    def update(cls, id, update_data):
        """Update a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        update_data['updated_at'] = datetime.utcnow()
        return cls.get_collection().update_one(
            {'_id': id},
            {'$set': update_data}
        )
    
    @classmethod
    def delete(cls, id):
        """Delete a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.get_collection().delete_one({'_id': id})
    
