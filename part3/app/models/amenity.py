#!/usr/bin/python3
""" Class User """

'''
Requiurements:
id (String): Unique identifier for each amenity.
name (String): The name of the amenity (e.g., "Wi-Fi", "Parking"). Required, maximum length of 50 characters.
created_at (DateTime): Timestamp when the amenity is created.
updated_at (DateTime): Timestamp when the amenity is last updated.
'''

from app.models.base import BaseModel
from app import db
from .base import BaseModel
from flask_sqlalchemy import SQLAlchemy

class Amenity(BaseModel):
    ''' Class Amenity, inherits from BaseModel '''
    
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Name is required and cannot exceed 50 characters")
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value
