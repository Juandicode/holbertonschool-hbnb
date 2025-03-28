#!/usr/bin/python3
"""Class User"""

import uuid
from app.models.base import BaseModel
from email_validator import validate_email, EmailNotValidError
from flask import current_app
from app import db, bcrypt
from sqlalchemy.orm import validates, relationship
from flask_sqlalchemy import SQLAlchemy


class User(BaseModel):
    """Class User, inherits from BaseModel"""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        try:
            email_info = validate_email(value, check_deliverability=False)  
            self._email = email_info.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")
        return value

    @validates('password')
    def validate_password(self, key, value):
        from app import bcrypt
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')
        return self._password
        
    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
