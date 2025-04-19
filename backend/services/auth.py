import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timezone, timedelta
from backend.models.mongodb.user import User
from backend.models.mongodb.role import Role, RoleName
from backend.repositories.user import UsersRepository
from backend.helpers.mail_gateway import MailGateway
from backend.helpers.utils import generate_password_hash, check_password_hash

load_dotenv()

class AuthService:
    JWT_PRIVATE_KEY = os.environ.get("JWT_PRIVATE_KEY", "")
    JWT_PUBLIC_KEY = os.environ.get("JWT_PUBLIC_KEY", "")
    ALGORITHM = os.environ.get("JWT_ALGORITHM", "RS256")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"))
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "example.com")
    FRONT_END_URL = os.environ.get("FRONT_END_URL", "http://localhost:3000")

    @classmethod
    def create_token(cls, data: dict, expires_delta):
        """
        Create a JWT access token using RS256.
        """
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + expires_delta  # Use timezone-aware datetime
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.JWT_PRIVATE_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def decode_token(cls, token: str):
        """
        Decode a JWT access token using RS256.
        """
        return jwt.decode(token, cls.JWT_PUBLIC_KEY, algorithms=[cls.ALGORITHM])
    
    @classmethod
    async def set_new_password(cls, token, data):
        decoded_token = AuthService.decode_token(token)

        if decoded_token.get("type") != "password_reset":
            raise Exception("Not a password reset token")

        user_email = decoded_token.get("sub")
        user = await UsersRepository.get_user_by_email(email=user_email)

        if not user:
            raise Exception(detail="User not found")

        if check_password_hash(decoded_token.get("password_hash"), user._password[16:32]):
            user.password = data.get("password")
            await UsersRepository.save(user)
        else:
            raise Exception("Password hash mismatch")

    @classmethod
    def send_password_reset_email(cls, email: str, reset_token: str):
        print(f"Sending password reset email to {email}")

        MailGateway.send(
            from_email=f'info@{cls.DOMAIN_NAME}',
            to_emails=[email],
            subject=f'{cls.DOMAIN_NAME} - Password reset',
            html_content=f"""
                <strong>
                    You sent a password reset request to {email}.
                </strong>
                <br>
                <br>
                <a href="{cls.FRONT_END_URL}/password-reset/password?token={reset_token}">Click here to reset your password</a>
                <p>{reset_token}</p>
            """
        )

    @classmethod
    async def request_password_reset(cls, email: str):
        """
        Send a password reset email to the user
        """
        print(f"Password reset request for email: {email}")

        user = await UsersRepository.get_user_by_email(email=email)
        if not user:
            return

        verification_token = cls.create_token(
            data={"sub": user.email, "type": "password_reset", "password_hash": generate_password_hash(user._password[16:32])},
            expires_delta=timedelta(hours=24)
        )
        cls.send_password_reset_email(user.email, verification_token)

    @classmethod
    async def verify_email(cls, token: str):
        """
        Verify a user's email address
        """
        decoded_token = cls.decode_token(token)

        if decoded_token.get("type") != "registration":
            raise Exception("Not a registration token")

        user_email = decoded_token.get("sub")

        user = await UsersRepository.get_user_by_email(email=user_email)

        if not user.has_role(Role(RoleName.UNVERIFIED)):
            raise Exception("User already verified")
        
        user.remove_role(Role(RoleName.UNVERIFIED))
        user.add_role(Role(RoleName.FREE))
        await UsersRepository.save(user)

    @classmethod
    async def register_email(cls, email: str, password: str):
        user = await UsersRepository.get_user_by_email(email=email)

        if not user:
            new_user = User(email=email, password=password)
            verification_token = cls.create_token(
                data={"sub": new_user.email, "type": "registration"},
                expires_delta=timedelta(hours=24)
            )
            await UsersRepository.save(new_user)
            cls.send_password_reset_email(new_user.email, verification_token)
            return {"message": "User created"}
        else:
            if not user.has_role(Role(RoleName.UNVERIFIED)):
                raise Exception("User already verified")

            verification_token = cls.create_token(
                data={"sub": user.email, "type": "registration"},
                expires_delta=timedelta(hours=24)
            )
            cls.send_password_reset_email(user.email, verification_token)
            return {"message": "User exists, resending verification email"}
            
    @classmethod
    async def login_user(cls, email: str, password: str):
        user = await UsersRepository.get_user_by_email(email=email)

        if user is None:
            raise Exception("User not found")
        
        if not check_password_hash(hashed_password=user._password, password=password):
            raise Exception("Invalid password")

        roles_list_str = [str(role) for role in user.get_roles()]
        
        access_token_expiration = timedelta(seconds=cls.JWT_ACCESS_TOKEN_EXPIRES)
        refresh_token_expiration = timedelta(seconds=cls.JWT_REFRESH_TOKEN_EXPIRES)
        access_token = cls.create_token(data={"sub": user.email, "roles": roles_list_str}, expires_delta=access_token_expiration)
        refresh_token = cls.create_token(data={"sub": user.email}, expires_delta=refresh_token_expiration)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    
    @classmethod
    async def register_user(cls, email: str, password: str):
        user = await UsersRepository.get_user_by_email(email=email)

        if user is not None:
            raise Exception("User already exists")
        
        # Create the user
        new_user = User(email=email, password=password)
        
        # Add the user as a free user
        new_user.add_role(Role(RoleName.FREE))
        await UsersRepository.save(new_user)
