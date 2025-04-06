from posixpath import join as posixpath_join
from uuid import uuid4
from passlib.context import CryptContext

# Create a password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def multi_urljoin(*parts):
    formatted_parts = []
    for part in parts:
        formatted_parts.append(part.rstrip('/').lstrip('/'))
    return posixpath_join(*formatted_parts)

def generate_id():
    return str(uuid4())

def generate_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)

def check_password_hash(hashed_password: str, password: str) -> bool:
    """
    Verify a password against its hash using bcrypt.
    """
    return pwd_context.verify(password, hashed_password)
