from app import create_app, db
from app.models import User, Place, Review, Amenity
# adapte le nom de ton modèle utilisateur

app = create_app()


def create_admin():
    """Créer un administrateur par défaut si aucun n’existe."""
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')  # selon ton implémentation
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin créé : admin@example.com / admin123")
        else:
            print("ℹ️ Admin déjà présent en base.")


if __name__ == '__main__':
    create_admin()
    app.run(debug=True)
