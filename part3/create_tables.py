from run import create_app
from app import db
from app.models import *  # importa todos los modelos para que SQLAlchemy los registre

app = create_app()

with app.app_context():
    db.create_all()
    print("Tablas creadas.")