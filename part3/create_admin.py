from app import create_app, db
from app.models.user import User

app = create_app()
app.app_context().push()

# Opcional: eliminar admin previo
user = User.query.filter_by(email="admin@example.com").first()
if user:
    db.session.delete(user)
    db.session.commit()

admin = User(
    first_name="Admin",
    last_name="User",
    email="admin@example.com",
    password="admin123",  # contraseña válida
    is_admin=True
)

db.session.add(admin)
db.session.commit()

print("Admin creado correctamente")