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
