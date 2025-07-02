from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api 

from config import DevelopmentConfig

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):  
    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API', description='API for managing places, users, reviews, and amenities')

    bcrypt.init_app(app)
    jwt.init_app(app)

    
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import auth_ns


    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(auth_ns, path='/auth')

    return app
