from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)

    def add_review(self, review):
        from app import db
        db.session.add(review)
        db.session.commit()

    def get_review_by_id(self, review_id):
        return self.model.query.get(review_id)

    def get_all_reviews(self):
        return self.model.query.all()

    def update_user(self, review_id, data):
        from app import db
        review = self.get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()

            
    def delete(self, review_id):
        from app import db
        obj = self.get(review_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()