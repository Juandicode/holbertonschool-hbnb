#!/usr/bin/python3
"""Place class"""
from app.models.base import BaseModel
import uuid
from app import db
from flask_sqlalchemy import SQLAlchemy

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model"""

    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary='place_amenity', backref='places', lazy=True)

    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner, description: str = ""):
        super().__init__()  # hereda id, created_at, updated_at
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self._amenities = []  # list for storing amenities
        self.reviews = []  # list for storing reviews
        owner.add_place(self)  # Automatically add this place to the owner list
    
 
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

    def validate_owner(self, value):       # Local import to avoid circular import
        from .user import User
        if not isinstance(value, User):
            raise ValueError("Owner must be a valid User instance")
        return value

    def add_review(self, review):
        """Añade una reseña a este lugar"""
        from .review import Review  # import local pa avoid circular import
        if not isinstance(review, Review):
            raise ValueError("Solo se pueden añadir instancias de Review")
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """add a  Amenity to place, validating is a valid Amenity instance"""
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Solo se aceptan instancias de Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Elimina un Amenity del lugar si existe"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    @property
    def amenities(self):
        return self._amenities

    def to_dict(self):
        """Returns a dictionary representation of the place"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            },
            "amenities": [
                {"id": amenity.id, "name": amenity.name}
                for amenity in self.amenities
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update_from_dict(self, data: dict, amenity_repo):
        if 'title' in data:
            self.title = self.validate_title(data['title'])
        if 'description' in data:
            self.description = self.validate_description(data['description'])
        if 'price' in data:
            self.price = self.validate_price(data['price'])
        if 'latitude' in data:
            self.latitude = self.validate_latitude(data['latitude'])
        if 'longitude' in data:
            self.longitude = self.validate_longitude(data['longitude'])

        if 'amenities' in data:
            self._amenities = []
            for amenity_id in data['amenities']:
                amenity = amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                self.add_amenity(amenity)


from app.models.amenity import Amenity