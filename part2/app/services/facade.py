from app.persistence.repository import InMemoryRepository
from app.models.users import User
from app.models.amenities import Amenity
from app.models.places import Place
from app.models.reviews import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # USER
    def create_user(self, user_data):
        user = User(**user_data)
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

    def get_all(self):
        return self.user_repo.get_all()

    # AMENITIES
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "").strip()
        if not name:
            raise ValueError("Amenity name cannot be empty.")
        amenity = Amenity(name=name)
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

def create_place(self, place_data):
    # Vérifications des champs obligatoires
    required_fields = ["title", "price", "latitude", "longitude", "owner_id", "amenities"]
    for field in required_fields:
        if field not in place_data:
            raise ValueError(f"{field} is required.")

    # Validation des valeurs
    price = float(place_data["price"])
    latitude = float(place_data["latitude"])
    longitude = float(place_data["longitude"])
    if price < 0:
        raise ValueError("Price must be non-negative.")
    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")

    # Vérifier l'existence du propriétaire
    owner = self.get_user(place_data["owner_id"])
    if not owner:
        raise ValueError("Owner not found.")

    # Récupérer les objets Amenity correctement
    amenities = []
    if place_data["amenities"]:
        for amenity_id in place_data["amenities"]:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id '{amenity_id}' not found.")
            amenities.append(amenity)

    # Créer l'objet Place
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
