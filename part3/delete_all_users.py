from hbnb_app import create_app, db
from hbnb_app.models.user import User

app = create_app()
with app.app_context():
    users = User.query.filter(User.email != "hacker@example.com").all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    print(f"Deleted {len(users)} non-admin users.")

