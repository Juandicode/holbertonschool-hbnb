from flask import Flask
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import JWTManager # new import from JWT
from app.api import api  # <-- importás el Api ya configurado con los namespaces

bcrypt = Bcrypt() # create bcrypt instance
jwt = JWTManager() 

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    api.init_app(app)  # <-- lo registrás en la app
    bcrypt.init_app(app)
    jwt.init_app(app)
    return app

