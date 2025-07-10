#!/usr/bin/python3
"""User class"""
import uuid
from .base import BaseModel
from hbnb_app import db, bcrypt
class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)    
    
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
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

    def hash_password(self, password: str):
        """hashes password before storing it in self. password"""
        from app import bcrypt
        if not password or not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be a string with at least 6 characters.")
        self.password = (
                bcrypt
                .generate_password_hash(password)
                .decode('utf-8') # correct way
        )

    def verify_password(self, password: str) -> bool: # verifies the password
        """verifies a password against the stored hash"""
        from app import bcrypt
        if not password:
            return False
        return bcrypt.check_password_hash(self.password, password) # ues flask-bcrpyt

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

