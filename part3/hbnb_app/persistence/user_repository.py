from hbnb_app.models.user import User
from hbnb_app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from hbnb_app import db


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str) -> User:
        """Busca un usuario por email"""
        return self.get_by_attribute('email', email)

    def exists_by_email(self, email: str) -> bool:
        """Retorna True si existe un usuario con ese email"""
        return db.session.query(
            self.model.query.filter_by(email=email).exists()
        ).scalar()

    def get_admin_users(self) -> list[User]:
        """Devuelve todos los usuarios con is_admin=True"""
        return self.model.query.filter_by(is_admin=True).all()
