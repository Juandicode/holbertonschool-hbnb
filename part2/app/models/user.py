#!/usr/bin/python3
"""User class"""

import uuid
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        """the super inherits from baseclass"""
        self.first_name = self.validate_name(first_name, 'First Name')
        self.last_name = self.validate_name(last_name, 'Last name')
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.places = []        # list to store places owned by user
        self.reviews = []  # list for reviews by user
    def validate_name(self, value, field_name):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError(f"{field_name} is required and cannot exceed 50 characters")
        return value

    def validate_email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required")
        if '@' not in value or '.' not in value:
            raise ValueError("Invalid email format")
        return value

    def validate_is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        return value
    
    def add_place(self, place):
        """Add a place to the user list of owned places"""
        from .place import Place    # Local import para evitar importacion circular
        if not isinstance(place, Place):
            raise ValueError("Can only add Place instances")
        if place not in self.places:
            self.places.append(place)
    
    def add_review(self, review):
        """add a review to the user list"""
        from .review import Review  # Import local
        if not isinstance(review, Review):
            raise ValueError("Solo se pueden añadir instancias de Review")
        if review not in self.reviews:
            self.reviews.append(review)