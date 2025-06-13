#!/usr/bin/python3
from .base import BaseModel
import uuid
class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not name:
            raise ValueError("Amenity name is required.")
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or fewer.")
        return name
