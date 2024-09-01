from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

db_mongo = PyMongo()
db = SQLAlchemy()
jwt = JWTManager()