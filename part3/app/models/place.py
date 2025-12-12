from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer
from app.extensions import db

"""
This module contains a representation of Place to rent
"""
place_amenity = db.Table(
    'place_amenity',
    Column('place_id', String, ForeignKey(
        'places.id'), primary_key=True, nullable=False),
    Column('amenity.id', String, ForeignKey(
        'amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    # price per nights
    longitude: Mapped[float] = mapped_column(nullable=False)
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="places")
    reviews = relationship('Review', back_populates='place')
    amenities = relationship(
        'Amenity', secondary=place_amenity,
        lazy="subquery", back_populates='places')

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        }
