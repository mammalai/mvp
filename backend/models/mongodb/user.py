import re
from backend.extensions import db_mongo
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from dataclasses import dataclass, asdict

def generate_uuid():
    return uuid4()

@dataclass
class MongoBaseClass():

    def dict(self):
        """a method to convert the dataclass to a dictionary"""
        return {k: v for k, v in asdict(self).items()}

    def save(self):
        NotImplementedError()

@dataclass
class User(MongoBaseClass, MongoClass2):
    
    __collectionname__ = "users"
    email:str
    _password:str
    id:str

    def __init__(self, email:str, password:str, id:str = None):
        if id == None:
            self.id = str(generate_uuid())
        else:
            self.id = id
        self.email = email
        self.password = password  # This calls the setter method

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
        print(value)
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
    def get_user_by_email(cls, email):
        """return the first user with this email"""
        user_dict = list(db_mongo.db.users.find({ "email": email }))[0]
        user_dict.pop("_id") # TO DO: You can remove this ID using a mongo DB query/projection
        user_dict["password"] = user_dict.pop("_password")
        return cls(**user_dict)

    def save(self):
        #using upsert here which means update if exists and insert if not
        db_mongo.db["__collectionname__"].replace_one({"id": self.id}, self.dict(), upsert=True)

    def delete(self):
        """delete the user from the database"""
        db_mongo.db["__collectionname__"].delete_one({"id": self.id})


"""
To create this table in the database

Run:
$ flask shell
>>> from backend.models.user import User
>>> db.create_all()
"""
