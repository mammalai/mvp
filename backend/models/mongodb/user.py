import re
from backend.extensions import db
from uuid import uuid4
from datetime import datetime

from dataclasses import dataclass, asdict

from .mongobase import MongoBaseClass
from passlib.context import CryptContext

def generate_uuid():
    return uuid4()

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password):
    return pwd_context.hash(password)

def check_password_hash(hashed_password, password):
    return pwd_context.verify(password, hashed_password)

@dataclass
class User(MongoBaseClass):
    __collectionname__ = "users"
    email: str
    _password: str
    id: str

    def __init__(self, email: str, id: str = None, password: str = None, _password: str = None):
        if id is None:
            self.id = str(generate_uuid())
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

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @classmethod
    async def get_user_by_email(cls, email):
        """return the first user with this email asynchronously"""
        query = await cls.query.filter_by(email=email)
        return await query.first()

    async def save(self):
        """Save the user to the database asynchronously"""
        # Using upsert here which means update if exists and insert if not
        await db[self.__collectionname__].replace_one(
            {"id": self.id}, 
            self.dict(), 
            upsert=True
        )

    async def delete(self):
        """Delete the user from the database asynchronously"""
        await db[self.__collectionname__].delete_one({"id": self.id})

