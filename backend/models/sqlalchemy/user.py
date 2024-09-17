import re
from backend.extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def generate_uuid():
    return uuid4()
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False)
    _password = db.Column(db.Text())

    def __init__(self, email:str, password:str):
        self.id=str(generate_uuid())
        self.email = email
        self._validate_strong_password(password)
        self._password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.email}>"

    # the @property and @password.setter are used to get and set the password - they will automatically validate and hash the password
    @property
    def password(self):
        """
            - The password property should not be accessed directly
            - It should only be set by the set_password method, and we will
            only return True or False to indicate if the password is set
        """
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
    def get_user_by_username(cls, username):
        """return the first user with this username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        """return the first user with this email"""
        return cls.query.filter_by(email=email).first()

    def save(self):
        """write user to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delte user from the database"""
        db.session.delete(self)
        db.session.commit()

"""
To create this table in the database

Run:
$ flask shell
>>> from backend.models.user import User
>>> db.create_all()
"""
