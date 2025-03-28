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
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        password = user_data.pop('password')
        new_user = facade.create_user({**user_data, 'password': password})
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name,
                'email': new_user.email}, 201

    def get(self):
        """Get all users"""
        users = facade.get_all()
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
    def put(self, user_id):
            """Update a User (Admins or user themselves only)"""
            current_user = get_jwt_identity()  #Obtener usuario autenticado

            if not current_user['is_admin'] and current_user['id'] != user_id: #verifica si el usuario es admin o el mismo usuario
                return {'error': 'Admin privileges required'}, 403

            user = facade.get_user(user_id) #obtiene el usuario
            if not user:
                return {'error': "User not found"}, 404

            data = api.payload #obtiene los datos del usuario
            updated_user = facade.update_user(user_id, data) #actualiza el usuario

            return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()  #permite a un usuario admin crear otros usuarios
    def post(self):
        """Admin creates a new user"""
        current_user = get_jwt_identity()
        if not current_user['is_admin']: #verifica si el usuario es admin
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json #obtiene los datos del usuario
        email = user_data.get('email')

        if facade.get_user_by_email(email): #verifica si el email ya esta registrado
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data) #crea el usuario
        return {'id': new_user.id, 'email': new_user.email}, 201
