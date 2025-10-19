from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.price = kwargs.get("price", 0.0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.longitude = kwargs.get("longitude", 0.0)
        self.owner = kwargs.get("owner", None)
        self.amenities = kwargs.get("amenities", [])
        self.reviews = kwargs.get("reviews", [])
        super().__init__()

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "amenities": [a.id for a in self.amenities],
            "reviews": [r.id for r in self.reviews]
        }
        return data
