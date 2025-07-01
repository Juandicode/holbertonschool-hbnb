from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api import api
from config import DevelopmentConfig  # ✅ importás la clase, no el string

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):  # ✅ usás la clase
    app = Flask(__name__)
    app.config.from_object(config_class)  # ✅ correcto, ahora sí es una clase
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    api.init_app(app)
    
    return app
