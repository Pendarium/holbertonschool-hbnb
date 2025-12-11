from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

# --- TOKEN IDENTITY
    @staticmethod
    def get_token_identity():
        identity = get_jwt_identity()
        claims = get_jwt()
        return {"id": identity, "role": claims.get("is_admin", False)}

# --- USER CRUD ----------------------------------
    def create_user(self, user_data):
        """
        This function create a new
        And save it in the repo
        """
        user = User(**user_data)
        user.hash_password(user.password)  # method from class User in models
        self.user_repo.add(user)  # method from repository class in persistence
        return user

    def get_user(self, user_id):
        """
        This function retrieve a user
        by its id
        """
        return self.user_repo.get(user_id)  # method from repo

    def get_user_by_email(self, email):
        """
        This function retrieve a user
        by its email
        """
        return self.user_repo.get_user_by_email(email)
    # method from user_repositoryf

    def get_all(self):
        """
        This function retrieve all users
        known in a list
        """
        return self.user_repo.get_all()  # method from repo

    def update(self, obj_id, data):
        """
        This function modify a user
        """
        return self.user_repo.update(obj_id, data)
    # method from repo

# --- AMENITY CRUD ----------------------------------

    def create_amenity(self, amenity_data):
        """Create an amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by its ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update a specific amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def get_by_attribute(self, attr_name, attr_value):
        """get an amenity by a specific attribute value"""
        return self.amenity_repo.get_by_attribute(attr_name, attr_value)

# --- PLACE CRUD ------------------------------------

    def create_place(self, place_data):
        """ Create a place"""
        # VALUES VALIDATIONS:
        if place_data["price"] <= 0:
            raise ValueError(
                "Invalid input data: price must be a positive float")
        if not -90 <= place_data["latitude"] <= 90:
            raise ValueError(
                "Invalid input data: latitude value must be between -90 and 90"
                )
        if not -180 <= place_data["longitude"] <= 180:
            raise ValueError(
                "Invalid input data: longitude value must be between "
                "-180 and 180"
            )
        # OWNER ID CHECK:
        owner_id = place_data.get("owner_id")
        if owner_id:
            if not self.user_repo.get(owner_id):
                raise LookupError(f"Owner is not found: {owner_id}")
        # AMENITY EXTRACT:
        amenities_ids = place_data.pop("amenities", None)
        # PLACE CREATION:
        place = Place(**place_data)
        # AMENITY LIST MANAGEMENT - attention à bien récupérer des objets
        # amenity quand la relationship sera fonctionnelle
        if amenities_ids:
            for id in amenities_ids:
                amenity = self.amenity_repo.get(id)
                if amenity:
                    place.add_amenity(amenity)
                else:
                    # CHECK AMENITY ID
                    raise LookupError(f"Amenity id not found:{id}")
        # SAVE PLACE
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by its ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        if "price" in place_data:
            if place_data["price"] <= 0:
                raise ValueError(
                    "Invalid input data: price must be a positive float")
        if "latitude" in place_data:
            if not -90 <= place_data["latitude"] <= 90:
                raise ValueError(
                    "Invalid input data: latitude value must be "
                    "between -90 and 90"
                    )
        if "longitude" in place_data:
            if not -180 <= place_data["longitude"] <= 180:
                raise ValueError(
                    "Invalid input data: longitude value must be between "
                    "-180 and 180"
                )
        return self.place_repo.update(place_id, place_data)

# --- REVIEW CRUD -------------------------------------

    def create_review(self, review_data):
        """ Create a review and add it to the place
        its linked to"""
        # RATING VALUE VALIDATION:
        if not 0 <= review_data['rating'] <= 5:
            raise ValueError("Bad request: rating must be between 0 and 5")
        # USER ID VERIFICATION:
        user_id = review_data['user_id']
        if not self.user_repo.get(user_id):
            raise LookupError(f"Owner id not found: {user_id}")
        # PLACE ID VERIFICATION:
        place_id = review_data['place_id']
        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError(f"Place id not found: {place_id}")
        # REVIEW CREATION:
        review = Review(**review_data)
        # ADDING REVIEW TO THE PLACE:
        # place.add_review(review.id)
        # REVIEW SAVING:
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by its ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # made directly in API - since it's 00h
        # I don't fix it now
        pass

    def update_review(self, review_id, review_data):
        """Update a review
        - review's id is needed so we know which review to update
        - datas to update are needed
        """
        if "rating" in review_data:
            if not 0 <= review_data['rating'] <= 5:
                raise ValueError("Bad request: rating must be between 0 and 5")
        if "comment" in review_data:
            if not isinstance(review_data["comment"], str):
                raise ValueError("Bad request: comment must be a string")
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """ Delete a review"""
        return self.review_repo.delete(review_id)
