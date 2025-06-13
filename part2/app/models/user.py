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
