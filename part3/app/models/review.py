#!/usr/bin/python3
"""Review class"""
from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text: str, rating: int, user, place):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user = self.validate_user(user)
        self.place = self.validate_place(place)

        # relaciones
        user.add_review(self)
        place.add_review(self)

    def validate_text(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Review text must be a non-empty string")
        return value.strip()

    def validate_rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return value

    def validate_user(self, value):
        from .user import User
        if not isinstance(value, User):
            raise ValueError("User must be a valid User instance")
        return value

    def validate_place(self, value):
        from .place import Place
        if not isinstance(value, Place):
            raise ValueError("Place must be a valid Place instance")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id,
            "place_id": self.place.id,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
            "place": {
                "id": self.place.id,
                "title": self.place.title
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

