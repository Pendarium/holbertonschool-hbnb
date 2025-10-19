from .base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.places = kwargs.get("places", [])
        super().__init__()

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        return data
