
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .place import place_amenity


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    places = relationship(
        "Place", secondary=place_amenity,
        back_populates='amenities')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
