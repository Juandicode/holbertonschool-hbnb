from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_by_email(self, email):
        """Buscar un usuario por su correo electrónico."""
        return self.model.query.filter_by(email=email).first()

    def add_user(self, user):
        from app import db
        db.session.add(user)
        db.session.commit()

    def get_user_by_id(self, user_id):
        return self.model.query.get(user_id)

    def get_all_users(self):
        return self.model.query.all()

    def update_user(self, user_id, data):
        from app import db
        user = self.get(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()