from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self,
                 user_id,
                 name,
                 city=None,
                 price_per_night=0,
                 **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.name = name
        self.city = city
        self.price_per_night = price_per_night
        self.reviews = []     # relation vers Review
        self.amenities = []   # relation vers Amenity
