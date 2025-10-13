from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self,
                 email,
                 password,
                 first_name=None,
                 last_name=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []   # relation vers les places
        self.reviews = []  # relation vers les reviews
