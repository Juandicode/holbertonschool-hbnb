#!/usr/bin/python3
"""Place class"""
from .base import BaseModel

class Place(BaseModel):
    """Place model"""
    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner: User, description: str = ""):
        super().__init__()  # hereda id, created_at, updated_at
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)

    def validate_title(self, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")
        return value

    def validate_description(self, value):
        if value is not None and not isinstance(value, str):    #si value no es none y n es un string 
            raise ValueError("Description must be a string")    #tira error 
        return value or ""                                      #si value es un string no vacio lo retorna, y sino retorna una cadena vacia 

    def validate_price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        return float(value)

    def validate_latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be a float between -90.0 and 90.0")
        return float(value)

    def validate_longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be a float between -180.0 and 180.0")
        return float(value)

    def validate_owner(self, value):
        from .user import User
        if not isinstance(value, User):
            raise ValueError("Owner must be a valid User instance")
        return value