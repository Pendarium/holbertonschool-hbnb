from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # Pas de table pour BaseModel directement

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp and persist the object in the DB"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the
        object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp and commit

    def is_max_length(self, name, value, max_length):
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.")

    def is_between(self, name, value, min_value, max_value):
        if not min_value < value < max_value:
            raise ValueError(
                f"{name} must be between {min_value} and {max_value}.")
