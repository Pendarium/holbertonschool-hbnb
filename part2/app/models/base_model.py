import uuid
from datetime import datetime


class base_model:
    def __init__(self, id=None, created_at=None, update_at=None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.update_at = update_at or datetime.now()

    def update(self, **kwargs):
        """Update instance attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.updated_at = datetime.now()
