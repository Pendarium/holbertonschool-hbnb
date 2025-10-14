from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text="", rating=0, place=None, user=None):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def is_valid(self):
        return isinstance(self.rating, (int, float)) and 1 <= self.rating <= 5
