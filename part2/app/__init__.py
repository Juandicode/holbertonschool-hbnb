from flask import Flask
from flask_bcrypt import Bcrypt # new import from bcrypt
from app.api import api  # <-- importás el Api ya configurado con los namespaces

bcrypt = Bcrypt() # create bcrypt instance

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    api.init_app(app)  # <-- lo registrás en la app
    bcrypt.init_app(app)

    return app
