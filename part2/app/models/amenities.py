from .base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.places = []

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)


def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
    pass


def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
    pass


def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
    pass


def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
    pass


def dict(self):
    return {
        "id": self.id,
        "name": self.name
    }
