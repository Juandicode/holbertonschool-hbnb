from app.persistence.repository import SQLAlchemyRepository
class AmenityRepo(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)
    
    def add_amenity(self, name):
        from app import db
        db.session.add(name)
        db.session.commit()

    def get_amenity_by_id(self, amenity_id):
        return self.model.query.get(amenity_id)
    
    def get_all_amenities(self):
        return self.model.query.all()
    
    def update_amenity(self, amenity_id, amenity_data):
        from app import db
        amenity = self.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            db.session.commit()