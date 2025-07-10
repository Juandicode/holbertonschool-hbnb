#!/usr/bin/python3
from .base import BaseModel
import uuid
from hbnb_app import db
class Amenity(BaseModel, db.Model):
    """Class Amenity """
    __tablename__ = 'amenity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    def validate_name(self, name):
        if not name:
            raise ValueError("Amenity name is required.")
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or fewer.")
        return name

    def to_dict(self):
        """Return a dictionary representation of the Amenity."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def update_from_dict(self, data):
        if 'name' in data:
            self.name = self.validate_name(data['name'])
