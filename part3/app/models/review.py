
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Review(BaseModel):
    __tablename__ = 'reviews'

    comment: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    place_id: Mapped[str] = mapped_column(
        ForeignKey('places.id'),
        nullable=False)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'),
        nullable=False)
    user = relationship('User', back_populates='reviews')
    place = relationship('Place', back_populates='reviews')

    def to_dict(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
