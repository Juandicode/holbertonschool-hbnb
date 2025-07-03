from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity {amenity_id} not found")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        amenity.update_from_dict(amenity_data)
        self.amenity_repo.update(amenity)
        return amenity

    # Place methods
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            description=place_data.get('description', '')
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                },
                'amenities': [{
                    'id': a.id,
                    'name': a.name
                } for a in place.amenities],
                'reviews': [{
                    'id': r.id,
                    'text': r.text,
                    'rating': r.rating,
                    'user_id': r.user.id
                } for r in place.reviews]
            }
        return None

    def get_all_places(self):
        return [{
            'id': p.id,
            'title': p.title,
            'latitude': p.latitude,
            'longitude': p.longitude
        } for p in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update_from_dict(place_data, self.amenity_repo)
        self.place_repo.update(place)
        return place

    def delete_place(self, place_id):
        """delete a place and all its associated reviews"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"place {place_id} not found")

        for review in list(place.reviews):
            self.delete_review(review.id)

        self.place_repo.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        """Create a new review with validation"""
        from app.models.review import Review 
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        if not all(field in review_data for field in required_fields):
            raise ValueError("Missing required fields")
        
        if not isinstance(review_data['text'], str) or len(review_data['text'].strip()) == 0:
            raise ValueError("Review text must be a non-empty string")
        
        if not isinstance(review_data['rating'], int) or not 1 <= review_data['rating'] <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User does not exist")
        
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place does not exist")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID with relationships"""
        review = self.review_repo.get(review_id)
        if review:
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'place': {
                    'id': review.place.id,
                    'title': review.place.title
                }
            }
        return None

    def get_all_reviews(self):
        """Get all reviews with basic info"""
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id,
            'place_id': r.place.id
        } for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id,
            'user_name': f"{r.user.first_name} {r.user.last_name}"
        } for r in place.reviews]

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        if 'text' in review_data:
            if not isinstance(review_data['text'], str) or len(review_data['text'].strip()) == 0:
                raise ValueError("Review text must be a non-empty string")
            review.text = review_data['text']
        
        if 'rating' in review_data:
            if not isinstance(review_data['rating'], int) or not 1 <= review_data['rating'] <= 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = review_data['rating']
        
        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Remove from place's reviews
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        
        # Remove from user's reviews
        if review in review.user.reviews:
            review.user.reviews.remove(review)
        
        self.review_repo.delete(review_id)

# Singleton instance
facade = HBnBFacade()
