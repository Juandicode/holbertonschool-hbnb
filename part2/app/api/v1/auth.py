from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
from app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

# Modelo de login
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
}, strict=True)

# Ruta /login
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        credentials = request.json
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })
        return {'access_token': access_token}, 200

# Ruta protegida
@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f"Hello, user {current_user['id']}"}, 200

# Exporta el namespace como api
api = auth_ns
