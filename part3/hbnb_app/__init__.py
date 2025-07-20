from flask import Flask, jsonify
from flask_restx import Api

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
    }
}
from config import DevelopmentConfig
from hbnb_app.extensions import bcrypt, jwt, db

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Import models for sqlalchemy to register
    import hbnb_app.models  

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

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API for managing places, users, reviews, and amenities',
        prefix='/api/v1',
        authorizations=authorizations,
        security='Bearer'
    )
    from hbnb_app.api.v1.places    import api as places_ns
    from hbnb_app.api.v1.users     import api as users_ns
    from hbnb_app.api.v1.reviews   import api as reviews_ns
    from hbnb_app.api.v1.amenities import api as amenities_ns
    from hbnb_app.api.v1.auth      import api as auth_ns

    api.add_namespace(users_ns,     path='/users')
    api.add_namespace(places_ns,    path='/places')
    api.add_namespace(reviews_ns,   path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(auth_ns,      path='/auth')

    return app
