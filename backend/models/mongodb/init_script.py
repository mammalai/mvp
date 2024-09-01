"""Start of initialization script for MongoDB"""
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
flaskdb = client["flask"]

flaskdb.list_collection_names()