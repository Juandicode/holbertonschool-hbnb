from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

# Modelo de login (para Swagger y validación)
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = request.get_json()

        #   search user by email
        user = facade.get_user_by_email(credentials['email'])

        #  verify existence and password
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        #   create token with id and is_admin
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        #  return token
        return {'access_token': access_token}, 200
