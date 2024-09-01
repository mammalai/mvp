import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DB_TYPE") == "mongodb":
    db = PyMongo()
else:
    db = SQLAlchemy()

# db_mongo = PyMongo()
# db = SQLAlchemy()
jwt = JWTManager()