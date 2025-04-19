import bcrypt
from uuid import uuid4

def multi_urljoin(*parts):
    formatted_parts = []
    for part in parts:
        formatted_parts.append(part.rstrip('/').lstrip('/'))
    return '/'.join(formatted_parts)

def generate_id():
    return str(uuid4())

# Use bcrypt directly instead of passlib
def generate_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def check_password_hash(hashed_password: str, password: str) -> bool:
    """Verify a password against its hash using bcrypt."""
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
