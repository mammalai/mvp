import re
from backend.extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def generate_uuid():
    return uuid4()
    

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(), primary_key=True, default=str(generate_uuid()))
    username = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False)
    _password = db.Column(db.Text())

    def __init__(self, email:str, password:str):
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
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class EmailVerification(db.Model):
    """
    Verify a user's email address before promoting a user's role from
    a "unverified" role to "free" roler
    """
    __tablename__ = "email_verification"
    email = db.Column(db.String(), primary_key=True, nullable=False)
    token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailVerification {self.email}: {self.token}>"
    
    @classmethod
    def get_email_verification_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def get_email_verification_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class EmailPasswordReset(db.Model):
    """A table to store password reset tokens for users"""

    __tablename__ = "password_reset"
    email = db.Column(db.String(), primary_key=True, nullable=False)
    token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<PasswordReset {self.email}: {self.token}>"

    @classmethod
    def get_epr_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_epr_by_token(cls, token):
        return cls.query.filter_by(token=token).first() 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
"""
To create this table in the database

Run:
$ flask shell
>>> from backend.models.user import User
>>> db.create_all()
"""
