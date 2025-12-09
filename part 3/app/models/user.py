from app import db, bcrypt
from .basemodel import BaseModel
import re


class User(BaseModel):
    __tablename__ = "users"

    # Colonnes SQLAlchemy
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user")

    # Relations
    places = db.relationship(
        "Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship(
        "Review", back_populates="user", cascade="all, delete-orphan")

    # ---------------- Init ----------------
    def __init__(
            self, username=None, first_name=None, last_name=None, email=None,
                 password=None, is_admin=False, role=None):
        super().__init__()
        self.username = username or "admin"
        self.first_name = first_name or "Admin"
        self.last_name = last_name or "User"
        self.email = email or "admin@example.com"
        self.password = password or "admin123"
        self.is_admin = is_admin
        self.role = role if role else ("admin" if is_admin else "user")

    # ---------------- Methods ----------------
    def set_password(self, password):
        """Hash the password before saving (compatible avec run.py)"""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        self.places.append(place)

    def add_review(self, review):
        self.reviews.append(review)

    def delete_review(self, review):
        self.reviews.remove(review)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
            "role": self.role
        }

    # ---------------- Validators ----------------
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError("Username must be a string")
        super().is_max_length("Username", value, 50)
        self._username = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length("First name", value, 50)
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length("Last name", value, 50)
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self._is_admin = value
