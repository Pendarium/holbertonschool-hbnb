from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
