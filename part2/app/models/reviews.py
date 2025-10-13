from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, user_id, place_id, text, rating, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.place_id = place_id
        self.text = text
        self.rating = rating  # entre 1 et 5
