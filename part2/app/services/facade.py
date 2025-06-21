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

    # services/facade.py
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
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
        """Get place by ID with relationships"""
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
                } for a in place.amenities]
            }
        return None

    def get_all_places(self):
        """Get all places with basic info"""
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
    """
    Crea una nueva revisión con validación de datos
    """
    # Importación diferida para evitar circularidad
    from app.models.review import Review
    
    # Validar usuario
    user = self.user_repo.get(review_data['user_id'])
    if not user:
        raise ValueError("User not found")
        
    # Validar lugar
    place = self.place_repo.get(review_data['place_id'])
    if not place:
        raise ValueError("Place not found")
    
    # Crear la revisión
    try:
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        
        # Guardar en el repositorio
        self.review_repo.add(review)
        return review
        
    except ValueError as e:
        raise ValueError(f"Validation error: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Type error: {str(e)}")

def get_review(self, review_id):
    """
    Obtiene una revisión por su ID
    """
    review = self.review_repo.get(review_id)
    if not review:
        raise ValueError("Review not found")
    return review

def get_all_reviews(self):
    """
    Obtiene todas las revisiones existentes
    """
    return self.review_repo.get_all()

def get_reviews_by_place(self, place_id):
    """
    Obtiene todas las revisiones de un lugar específico
    """
    place = self.place_repo.get(place_id)
    if not place:
        raise ValueError("Place not found")
    
    # Asumiendo que Place tiene una propiedad reviews que lista las revisiones
    return place.reviews

def update_review(self, review_id, review_data):
    """
    Actualiza una revisión existente
    """
    review = self.review_repo.get(review_id)
    if not review:
        raise ValueError("Review not found")
    
    try:
        # Actualizar campos si están presentes en los datos
        if 'text' in review_data and review_data['text'] is not None:
            review.text = review.validate_text(review_data['text'])
        if 'rating' in review_data and review_data['rating'] is not None:
            review.rating = review.validate_rating(review_data['rating'])
        
        # Guardar cambios
        self.review_repo.update(review)
        return review
        
    except ValueError as e:
        raise ValueError(f"Validation error: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Type error: {str(e)}")

def delete_review(self, review_id):
    """
    Elimina una revisión y sus referencias asociadas
    """
    review = self.review_repo.get(review_id)
    if not review:
        raise ValueError("Review not found")
    
    # Eliminar referencias del lugar y usuario
    if review in review.place.reviews:
        review.place.reviews.remove(review)
    if review in review.user.reviews:
        review.user.reviews.remove(review)
    
    # Eliminar del repositorio
    self.review_repo.delete(review_id)

facade = HBnBFacade()
