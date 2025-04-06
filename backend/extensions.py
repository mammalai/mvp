import os
from fastapi import HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
if os.environ.get("DB_TYPE") == "mongodb":
    print("Using MongoDB")
    mongo_client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
    db = mongo_client[os.environ.get("MONGO_DB_NAME")]
else:
    raise Exception("DB_TYPE must be set to 'mongodb' in configuration.")
