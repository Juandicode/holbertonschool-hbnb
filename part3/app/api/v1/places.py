from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload
        existing_place = facade.get_place(data['title'])
        current_user = get_jwt_identity()
        user_id = current_user['id']
        data['owner_id'] = user_id
        
        if existing_place:
            return {'error': 'Place already exists'}, 400
        
        owner = facade.get_user(user_id)
        
        if not owner:
            return {'error': 'Owner not found'}, 404

        data.pop('owner_id')
        data['owner'] = owner
        n_place = facade.create_place(data)
        return {
            'place_id': n_place.id,
            'title': n_place.title,
            'description': n_place.description,
            'price': n_place.price,
            'latitude': n_place.latitude,
            'longitude': n_place.longitude,
            'owner_id': owner.id
        }, 201            

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude} for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner': {'id': place.owner.id, 'first_name': place.owner.first_name, 'last_name': place.owner.last_name, 'email': place.owner.email}}, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'place not found'}, 404

        if place.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        if not data or not isinstance(data, dict):
            return {'error': 'Invalid input data. Expected JSON object.'}, 400

        updated_place = facade.update_place(place_id, data)

        if not updated_place:
            return {'error': 'Input not valid'}, 400

        return {'message': 'Place updated successfully'}, 200

@api.route('/<place_id>')
class AdminPlaceDelete(Resource):
    @jwt_required()
    def delete(self, place_id):
        """Admins can delete any place"""
        current_user = get_jwt_identity() #obtiene el usuario actual
        is_admin = current_user['is_admin'] #verifica si el usuario es admin

        place = facade.get_place(place_id) #obtiene el place a eliminar
        if not place:
            return {'error': 'Place not found'}, 404 #si no existe el place

        if not is_admin: #si el usuario no es admin 
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
