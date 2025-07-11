from hbnb_app.persistence.user_repository import UserRepository
from hbnb_app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from hbnb_app.models.user    import User
from hbnb_app.models.amenity import Amenity
from hbnb_app.models.place   import Place
from hbnb_app.models.review  import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()  # Se mantiene porque es específico
        self.place_repo   = SQLAlchemyRepository(Place)
        self.review_repo  = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    
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
        # update expects (id, data)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # Place methods
    def create_place(self, place_data):
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            description=place_data.get('description', '')
        )
        for a in amenities:
            place.add_amenity(a)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        # Handle amenities update with proper objects
        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                amenities.append(amenity)
            place_data = dict(place_data)  # avoid mutating input
            place_data['amenities'] = amenities
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

# Singleton instance
facade = HBnBFacade()

