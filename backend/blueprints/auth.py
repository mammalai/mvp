from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from backend.services.auth import AuthService
from backend.repositories.user import UsersRepository

auth_router = APIRouter()

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

@auth_router.post("/password")
async def password_reset_new_password(request: Request):
    """
    Update the user's password with a new password
    """
    reset_token = request.query_params.get("token")
    data = await request.json()
    
    try:
        await AuthService.set_new_password(reset_token, data)
        return {"message": "Password reset successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid or expired token") from e


@auth_router.post("/password/reset", status_code=201)
async def password_reset_request_email(request: Request):
    """
    Send a password reset email to the user
    """
    data = await request.json()
    email = data.get("email")
    
    try:
        await AuthService.request_password_reset(email=email)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Password reset request failed") from e


@auth_router.post("/verification", status_code=201)
async def email_verification(request: Request):
    """
    Verify a user's email address
    """
    verification_token = request.query_params.get("token")

    try:
        await AuthService.verify_email(token=verification_token)
        return {"message": "Email verification successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email verification failed") from e


@auth_router.post("/registration", status_code=201)
async def email_registration(request: Request):
    data = await request.json()

    try:
        message = await AuthService.register_email(email=data.get("email"), password=data.get("password"))
        return message
    except Exception as e:
        raise HTTPException(status_code=400, detail="Registration failed") from e


@auth_router.post("/login")
async def login_user(request: Request, response: Response):
    data = await request.json()

    try:
        tokens = await AuthService.login_user(data.get("email"), data.get("password"))
        response.set_cookie("refresh_token", tokens["refresh_token"], httponly=True, samesite="Strict")
        return {"message": "Authentication successful", "access_token": tokens["access_token"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid username or password") from e


@auth_router.get("/whoami")
async def whoami(current_user: str = Depends(decode_access_token)):
    return current_user.safe_dict()


@auth_router.post("/register")
async def register_user(request: Request):
    data = await request.json()

    try:
        AuthService.register_user(data.get("email"), data.get("password"))
        return {"message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Registration failed") from e
    