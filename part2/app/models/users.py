from .base_model import BaseModel


class User(BaseModel):
    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.is_admin = kwargs.get("is_admin", False)
        self.places = kwargs.get("places", [])
        self.reviews = kwargs.get("reviews", [])
        super().__init__()

    def add_place(self, place):
        self.places.append(place)

    def add_review(self, review):
        self.reviews.append(review)

    def to_dict(self):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
        return data
