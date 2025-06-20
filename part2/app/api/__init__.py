# app/api/__init__.py

from flask import Flask
from flask_restx import Api

# 1. Import your namespaces
from app.api.v1.amenities import api as amenities_ns
# from app.api.v1.users     import api as users_ns
# from app.api.v1.places    import api as places_ns
# etc.

def create_app():
    """Factory to create and configure the Flask application."""
    app = Flask(__name__)

    # 2. Instantiate the RESTx API
    api = Api(
        app,
        version='1.0',
        title='HBnB REST API',
        description='Version 1 of the HBnB API'
    )

    # 3. Register namespaces with their URL prefixes
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # api.add_namespace(users_ns,      path='/api/v1/users')
    # api.add_namespace(places_ns,     path='/api/v1/places')

    return app

