#!/usr/bin/python3
from .base import BaseModel
import uuid
class Review(BaseModel):
    def __init__(self, text: str, rating: int, place, user):   
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)
<<<<<<< HEAD
        # para vincular automaticamente la reseña con el place y el user
        place.add_review(self)
        user.add_review(self)  
=======

        if self not in place.reviews:
            place.reviews.append(self)

>>>>>>> 12a03cacba771a2c307f5116eafe2c50345a81c2
    def validate_text(self, text):
        if not text:
            raise ValueError("Review text is required.")
        if len(text) > 1024:
            raise ValueError("Review text must be 1024 characters or fewer.")
        return text

    def validate_rating(self, rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating

    def validate_place(self, place):
        # Validamos que sea una instancia de la clase Place
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Place must be an instance of Place.")
        return place

    def validate_user(self, user):
        from app.models.user import User
        if not isinstance(user, User):
            raise TypeError("User must be an instance of User.")
        return user
