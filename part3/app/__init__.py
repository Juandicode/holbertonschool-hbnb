from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy         # Import SQLAlchemy
from config import DevelopmentConfig
from flask import Flask, Blueprint, jsonify
bcrypt = Bcrypt()
jwt    = JWTManager()
db     = SQLAlchemy()                          # Crear instancia de SQLAlchemy

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)                            # Conectar SQLAlchemy con Flask
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(app,
            version='1.0',
            title='HBnB API',
            description='API for managing places, users, reviews, and amenities',
            prefix='/api/v1')
    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({'msg': 'Missing Authorization Header'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({'msg': 'Invalid token'}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'msg': 'Token has expired'}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'msg': 'Token has been revoked'}), 401

    # Importar y registrar namespaces
    from app.api.v1.users     import api as users_ns
    from app.api.v1.places    import api as places_ns
    from app.api.v1.reviews   import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth      import auth_ns

    api.add_namespace(users_ns,     path='/users')
    api.add_namespace(places_ns,    path='/places')
    api.add_namespace(reviews_ns,   path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(auth_ns,      path='/auth')

    app.register_blueprint(blueprint)

    return app

