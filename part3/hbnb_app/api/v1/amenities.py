from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb_app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        data = request.get_json()

        current_user = get_jwt_identity()
        owner_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        data['owner_id'] = owner_id

        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get details of a single amenity by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return amenity.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an existing amenity"""
        try:
            data = request.get_json()

            amenity = facade.get_amenity(amenity_id)

            current_user = get_jwt_identity()
            user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
            is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False

            if str(amenity.owner_id) != str(user_id) and not is_admin:
                api.abort(403, "You are not allowed to modify this amenity")

            updated = facade.update_amenity(amenity_id, data)
            return updated.to_dict(), 200

        except ValueError as e:
            code = 404 if "not found" in str(e).lower() else 400
            api.abort(code, str(e))
