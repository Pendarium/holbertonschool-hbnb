from .basemodel import BaseModel
from app import db


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship(
        "Review", back_populates="place", cascade="all, delete-orphan"
    )
    amenities = db.relationship(
        "Amenity", secondary="place_amenity", back_populates="places")

    def __init__(
            self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.description = description

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Title must be a non-empty string")
        super().is_max_length("title", value, 100)
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        value = float(value)
        super().is_between("latitude", value, -90, 90)
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        value = float(value)
        super().is_between("longitude", value, -180, 180)
        self._longitude = value

    # ---------------- Methods ----------------
    def add_review(self, review):
        self.reviews.append(review)

    def delete_review(self, review):
        self.reviews.remove(review)

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
            "owner_id": self.owner.id,
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews],
        }
