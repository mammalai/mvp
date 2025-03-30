import os
from fastapi import HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

# MongoDB setup
if os.environ.get("DB_TYPE") == "mongodb":
    print("Using MongoDB")
    mongo_client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
    db = mongo_client[os.environ.get("MONGO_DB_NAME")]
else:
    raise Exception("DB_TYPE must be set to 'mongodb' in configuration.")

# JWT setup
JWT_PRIVATE_KEY = os.environ.get("JWT_PRIVATE_KEY", "")
JWT_PUBLIC_KEY = os.environ.get("JWT_PUBLIC_KEY", "")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "RS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict, expires_delta):
    """
    Create a JWT access token using RS256.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta  # Use timezone-aware datetime
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """
    Decode a JWT access token using RS256.
    """
    return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[ALGORITHM])

def decode_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header[len("Bearer "):]

    try:
        payload = decode_token(token)
        user_email = payload.get("sub")  # commonly "sub" is used for user identity
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user information",
            )
        return user_email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
