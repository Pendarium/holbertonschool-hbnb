from app.persistence.repository import InMemoryRepository
from app.models.users import User
from app.models.amenities import Amenity
from app.models.places import Place
from app.models.reviews import Review
import re


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # --- Email validator ---
    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    # --- Users ---
    def create_user(self, user_data):
        email = user_data.get("email", "").strip()
        if not email or not self._is_valid_email(email):
            raise ValueError("Invalid email format.")

        if self.get_user_by_email(email):
            raise ValueError("Email already registered.")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def update_user(self, user_id, user_data):
        if "email" in user_data:
            email = user_data["email"].strip()
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format.")
            existing_user = self.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered.")

        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all(self):
        return self.user_repo.get_all()

    # --- Amenities ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "").strip()
        if not name:
            raise ValueError("Amenity name cannot be empty.")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        name = amenity_data.get("name", "").strip()
        if not name:
            raise ValueError("Amenity name cannot be empty.")
        amenity.name = name
        self.amenity_repo.update(amenity.id, {"name": amenity.name})
        return amenity

    # --- Places ---
    def create_place(self, place_data):
        required_fields = ["title", "price", "latitude",
                           "longitude", "owner_id", "amenities"]
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"{field} is required.")

        price = float(place_data["price"])
        latitude = float(place_data["latitude"])
        longitude = float(place_data["longitude"])
        if price < 0:
            raise ValueError("Price must be non-negative.")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")

        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        amenities = []
        for amenity_id in place_data["amenities"]:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id '{amenity_id}' not found.")
            amenities.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner,
            amenities=amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        updated_fields = {}

        if "title" in place_data:
            updated_fields["title"] = place_data["title"]
        if "description" in place_data:
            updated_fields["description"] = place_data["description"]

        if "price" in place_data:
            try:
                price = float(place_data["price"])
            except (ValueError, TypeError):
                raise ValueError("Price must be a number.")
            if price < 0:
                raise ValueError("Price must be non-negative.")
            updated_fields["price"] = price

        if "latitude" in place_data:
            try:
                latitude = float(place_data["latitude"])
            except (ValueError, TypeError):
                raise ValueError("Latitude must be a number.")
            if not -90 <= latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90.")
            updated_fields["latitude"] = latitude

        if "longitude" in place_data:
            try:
                longitude = float(place_data["longitude"])
            except (ValueError, TypeError):
                raise ValueError("Longitude must be a number.")
            if not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180.")
            updated_fields["longitude"] = longitude

        if "owner_id" in place_data:
            owner = self.get_user(place_data["owner_id"])
            if not owner:
                raise ValueError("Owner not found.")
            updated_fields["owner"] = owner

        if "amenities" in place_data:
            if not isinstance(place_data["amenities"], (list, tuple)):
                raise ValueError("Amenities must be a list of IDs.")
            amenities_objs = []
            for aid in place_data["amenities"]:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise ValueError(f"Amenity with id '{aid}' not found.")
                amenities_objs.append(amenity)
            updated_fields["amenities"] = amenities_objs

        self.place_repo.update(place_id, updated_fields)
        return self.get_place(place_id)

    # --- Reviews ---
    def create_review(self, review_data):
        required_fields = ["text", "user_id", "place_id"]
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"{field} is required.")

        user = self.get_user(review_data["user_id"])
        if not user:
            raise ValueError("User not found.")

        place = self.get_place(review_data["place_id"])
        if not place:
            raise ValueError("Place not found.")

        review = Review(**review_data)
        self.review_repo.add(review)
        place.add_review(review)
        user.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)
