#!/usr/bin/python3

"""User class"""

import uuid
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init()
        """the super inherits from baseclass"""
        self.first_name = self.validate_name(first_name, 'First Name')
        self.last_name = self.validate_name(last_name, 'Last name')
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    def validate_first_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        return value

    def validate_last_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
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
