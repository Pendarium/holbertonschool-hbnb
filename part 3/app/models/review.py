from .basemodel import BaseModel
from app import db


class Review(BaseModel, db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(
        db.Integer, db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id,
            "user_id": self.user.id
        }
