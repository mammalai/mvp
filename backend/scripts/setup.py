import sys
import os

# Add the parent directory to the Python path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now we can import backend modules
from backend.models.mongodb.user import User
from backend.models.mongodb.role import Role, RoleName
from backend.repositories.user import UsersRepository
from backend.extensions import db  # We need this to establish the database connection

import secrets

def generate_secure_password(length):
    """
    Generate a cryptographically secure random password of the specified length.
    
    Args:
        length (int): The length of the password to generate
        
    Returns:
        str: A secure random password
    """
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    # Use the secrets module for cryptographically secure random selection
    password = ''.join(secrets.choice(charset) for _ in range(length))
    
    return password

async def create_admin_user(identity, strong_password):
    admin_user = User(email=identity, password=strong_password, roles=[Role(RoleName.ADMIN)])
    await UsersRepository.save(admin_user)
    return admin_user

admin_emails = [
    "salar.satti@nook.health",
    "bo.lemmens@nook.health",
    "carlos.mondragon@nook.health",
]

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    # Make sure environment variables are loaded
    load_dotenv()

    async def main():
        print("Starting admin user setup...")
        
        # Check DB connection
        try:
            # Print a confirmation
            print(f"Connected to database: {db.name}")
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            return
            
        for email in admin_emails:
            try:
                strong_password = generate_secure_password(16)
                admin_user = await create_admin_user(email, strong_password)
                print(f"Created admin user: {admin_user.email} with password: {strong_password}")
            except Exception as e:
                print(f"Error creating admin user {email}: {str(e)}")

    asyncio.run(main())
