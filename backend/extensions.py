import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DB_TYPE") == "mongodb":
    print("Using MongoDB")
    db = PyMongo()
elif os.environ.get("DB_TYPE") == "sqlalchemy":
    print("Using SQLAlchemy")
    db = SQLAlchemy()
else:
    raise Exception("DB_TYPE not set in configuration.")

jwt = JWTManager()