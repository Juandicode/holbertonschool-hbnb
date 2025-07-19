from hbnb_app import create_app, db
from hbnb_app.models.review import Review

app = create_app()

with app.app_context():
    orphans = Review.query.filter_by(place_id=None).all()
    print(f"Found {len(orphans)} orphan reviews.")

    for r in orphans:
        print(f"Deleting Review ID {r.id}: {r.text}")
        db.session.delete(r)
    db.session.commit()
    print("Orphan reviews deleted.")

