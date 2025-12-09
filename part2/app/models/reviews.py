from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, **kwargs):
        self.comment = kwargs.get("comment", "")
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        self.rating = kwargs.get("rating", None)
        super().__init__()

    def to_dict(self):
        data = {
            "id": self.id,
            "comment": self.comment,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating
        }
        return data
