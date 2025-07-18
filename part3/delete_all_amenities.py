from hbnb_app import create_app, db
from hbnb_app.models.amenity import Amenity

# Create and push app context
app = create_app()
app.app_context().push()

# Delete all amenities
Amenity.query.delete()
db.session.commit()

print("All amenities deleted successfully.")

