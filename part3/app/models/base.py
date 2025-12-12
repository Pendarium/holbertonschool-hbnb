
import uuid
from datetime import datetime
from app.extensions import db
"""
This module contains the basemodel class for
models objetcs.
"""


class BaseModel(db.Model):
    __abstract__ = True  # means it's an abstract class > no table created

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        # data is a dict with key and value to modify
        """Update the attributes of
        the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                # is key in data in self ?
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
