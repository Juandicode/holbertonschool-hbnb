from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)

    def add_Place(self, place):
        from app import db
        db.session.add(place)
        db.session.commit()

    def get_place_by_id(self, place_id):
        return self.model.query.get(place_id)

    def get_all_place(self):
        return self.model.query.all()

    def update_place(self, place_id, data):
        from app import db
        place = self.get(place_id)
        if place:
            for key, value in data.items():
                setattr(place, key, value)
            db.session.commit()

            
    def delete(self, place_id):
        from app import db
        place = self.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()