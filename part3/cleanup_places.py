from hbnb_app import create_app, db
from hbnb_app.models.place import Place
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

with app.app_context():
    places_sin_owner = Place.query.filter_by(owner=None).all()
    print(f"Encontrados {len(places_sin_owner)} lugares sin owner.")
    
    for place in places_sin_owner:
        print(f"Eliminando Place ID: {place.id} - Título: {place.title}")
        db.session.delete(place)
    
    db.session.commit()
    print("✅ Todos los lugares sin owner fueron eliminados.")

