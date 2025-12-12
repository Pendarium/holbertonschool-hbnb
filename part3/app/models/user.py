
from .base import BaseModel
from app.extensions import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String


class User(BaseModel):
    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False)
    places = relationship('Place', back_populates="owner", lazy=True)
    reviews = relationship('Review', back_populates="user", lazy=True)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_place(self, place):
        self.places.append(place)

    def to_dict(self):
        """
        This function allow to display some specific attribute of user.
        Usefull to avoid to return passwords, for example (will be implemented
        later)"""
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "is_admin": self.is_admin,
            # "places": [place.to_dict() for place in self.places],
            # "reviews": [review.to_dict() for review in self.reviews]
            }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
