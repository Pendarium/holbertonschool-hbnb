from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ------------------ USER ------------------ #
    def create_user(self, user_data):
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=user_data.get("is_admin", False)
        )
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    # ------------------ AMENITY ------------------ #
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # ------------------ PLACE ------------------ #
    def create_place(self, place_data):
        user = self.user_repo.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        del place_data['owner_id']
        place_data['owner'] = user

        amenity_ids = place_data.pop('amenities', None)
        place = Place(**place_data)
        self.place_repo.add(place)
        user.add_place(place)

        if amenity_ids:
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise KeyError(f"Amenity {amenity_id} not found")
                place.add_amenity(amenity)

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")

        # Mettre à jour les attributs simples
        for key, value in place_data.items():
            if key == 'amenities':
                # remplacer les amenities existants
                place.amenities = []
                for a in value:
                    amenity = self.get_amenity(a['id'])
                    if not amenity:
                        raise KeyError(f"Amenity {a['id']} not found")
                    place.add_amenity(amenity)
            elif hasattr(place, key):
                setattr(place, key, value)

        return place

    # ------------------ REVIEWS ------------------ #
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data')
        del review_data['user_id']
        review_data['user'] = user

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')
        del review_data['place_id']
        review_data['place'] = place

        if place.owner.id == user.id:
            raise ValueError('User cannot review their own place')

        # Vérifie si l'utilisateur a déjà fait un review
        for r in place.reviews:
            if r.user.id == user.id:
                raise ValueError('User has already reviewed this place')

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise KeyError('Review not found')

        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.delete_review(review)
        place.delete_review(review)
        self.review_repo.delete(review_id)
