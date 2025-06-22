from flask import Flask
from app.api import api  # <-- importás el Api ya configurado con los namespaces

def create_app():
    app = Flask(__name__)
    api.init_app(app)  # <-- lo registrás en la app
    return app