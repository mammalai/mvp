from fastapi import Request, HTTPException, status
from backend.services.auth import AuthService
from backend.repositories.user import UsersRepository

async def decode_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header[len("Bearer "):]

    try:
        payload = AuthService.decode_token(token)
        user_email = payload.get("sub")  # commonly "sub" is used for user identity
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user information",
            )
        # Check if the user exists in the database
        user = await UsersRepository.get_user_by_email(user_email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
