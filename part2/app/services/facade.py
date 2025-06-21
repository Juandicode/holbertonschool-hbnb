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

    # Placeholder method for creating a user

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # amenity part

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            amenity.name = amenity.validate_name(amenity_data['name'])

        self.amenity_repo.update(amenity)
        return amenity

    # Place-related methods
    def create_place(self, place_data):
        # Validate owner
        owner = self.user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        # Validate amenities
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        # Create place instance
        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            description=place_data.get('description', '')
        )

        # Associate amenities
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None


        # Update simple fields
        if 'title' in place_data:
            place.title = place.validate_title(place_data['title'])
        if 'description' in place_data:
            place.description = place.validate_description(place_data['description'])
        if 'price' in place_data:
            place.price = place.validate_price(place_data['price'])
        if 'latitude' in place_data:
            place.latitude = place.validate_latitude(place_data['latitude'])
        if 'longitude' in place_data:
            place.longitude = place.validate_longitude(place_data['longitude'])

        # Update amenities list
        if 'amenities' in place_data:
            # reset amenities
            place._amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                place.add_amenity(amenity)

        self.place_repo.update(place)
        return place

def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
    pass

def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
    pass

def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
    pass

def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
    pass

def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
    pass

def delete_review(self, review_id):
    # Placeholder for logic to delete a review
    pass

facade = HBnBFacade()
