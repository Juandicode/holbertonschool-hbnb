#!/usr/bin/python3
from hbnb_app import db, create_app  # Asegurate que tu app esté en create_app()
from hbnb_app.models.review import Review

app = create_app()

def delete_all_reviews():
    try:
        num_deleted = db.session.query(Review).delete()
        db.session.commit()
        print(f"✅ {num_deleted} reviews deleted successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Failed to delete reviews: {e}")

if __name__ == "__main__":
    with app.app_context():
        delete_all_reviews()

