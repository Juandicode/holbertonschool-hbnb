from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user"""
        current_user = get_jwt_identity()  # Get the authenticated user
        if not current_user['is_admin']:  # Check if the user is an admin
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Create the user with the hashed password
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        # Do not return the password in the response
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name,
                'email': new_user.email}, 201
    

    @api.response(200, 'User list retrieved successfully')
    @api.response(404, 'No users found')    
    def get(self):
        """Get all users"""
        users = facade.user_repo.get_all()
        if not users:
            return {'error': 'No users found'}, 404
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404
        
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200


    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User is successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, user_id):
            """Update a User (Admins or user themselves only)"""
            current_user = get_jwt_identity()  #Obtener usuario autenticado

            if not current_user['is_admin'] and current_user['id'] != user_id: #verifica si el usuario es admin o el mismo usuario
                return {'error': 'Admin privileges required'}, 403

            user = facade.get_user(user_id) #obtiene el usuario
            if not user:
                return {'error': "User not found"}, 404

            data = api.payload #obtiene los datos del usuario
            try:
                updated_user = facade.update_user(user_id, data) #actualiza el usuario
            except ValueError:
                return {'error': 'Invalid input data'}, 400

            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200