import re
from uuid import uuid4
from dataclasses import dataclass
from backend.helpers.utils import generate_id, generate_password_hash

@dataclass
class User():
    def __init__(self, email: str, id: str = None, password: str = None, _password: str = None):
        if id is None:
            self.id = generate_id()
        else:
            self.id = id
        self.email = email

        if password is not None:
            self.password = password  # This calls the setter method
        elif _password is not None:
            self._password = _password  # Initialize from the database
        else:
            raise TypeError("Password or _password (the hash of the password) must be provided")

    def __repr__(self):
        return f"<User {self.email}>"

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "_password": self._password,  # Store the hashed password
        }

    @property
    def password(self):
        return self._password is not None

    @password.setter
    def password(self, value):
        self._validate_strong_password(value)
        self._password = generate_password_hash(value)

    def _validate_strong_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")

