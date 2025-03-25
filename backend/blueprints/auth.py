from fastapi import APIRouter, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, decode
from backend.models import User, Role
from backend.extensions import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

auth_router = APIRouter()

@auth_router.post("/password")
async def password_reset_new_password(request: Request):
    """
    Update the user's password with a new password
    """
    reset_token = request.query_params.get("token")
    data = await request.json()

    try:
        decoded_token = decode(reset_token, options={"verify_signature": False})
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if decoded_token.get("type") != "password_reset":
        raise HTTPException(status_code=401, detail="Not a password reset token")

    user_email = decoded_token.get("sub")
    user = User.get_user_by_email(email=user_email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if check_password_hash(decoded_token.get("password_hash"), user._password[16:32]):
        user.password = data.get("password")
        user.save()
        return {"message": "Password reset successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")


def send_password_reset_email(email: str, reset_token: str):
    print(f"Sending password reset email to {email}")

    if os.environ.get("FLASK_ENV") in ["TEST", None]:
        return

    message = Mail(
        from_email=f'info@{os.environ.get("DOMAIN_NAME")}',
        to_emails=email,
        subject=f'{os.environ.get("DOMAIN_NAME")} - Password reset',
        html_content=f"""
            <strong>
                You sent a password reset request to {email}.
            </strong>
            <br>
            <br>
            <a href="{os.environ.get('FRONT_END_URL')}/password-reset/password?token={reset_token}">Click here to reset your password</a>
            <p>{reset_token}</p>
        """
    )
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if sendgrid_api_key:
        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            sg.send(message)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error sending email")
    else:
        raise HTTPException(status_code=500, detail="No SendGrid API key found")


@auth_router.post("/password/reset")
async def password_reset_request_email(request: Request):
    """
    Send a password reset email to the user
    """
    data = await request.json()
    email = data.get("email")
    print(f"Password reset request for email: {email}")

    user = User.get_user_by_email(email=email)
    if not user:
        return {"message": "Password reset email sent"}

    verification_token = jwt.create_access_token(
        identity=user.email,
        additional_claims={"type": "password_reset", "password_hash": generate_password_hash(user._password[16:32])},
        expires_delta=timedelta(hours=24)
    )
    send_password_reset_email(user.email, verification_token)
    return {"message": "Password reset email sent"}


@auth_router.post("/verification")
async def email_verification(request: Request):
    """
    Verify a user's email address
    """
    verification_token = request.query_params.get("token")

    try:
        decoded_token = decode(verification_token, options={"verify_signature": False})
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if decoded_token.get("type") != "registration":
        raise HTTPException(status_code=401, detail="Not a registration token")

    user_email = decoded_token.get("sub")
    user_roles = Role.get_all_roles_for_user(username=user_email)

    if len(user_roles) == 1 and user_roles[0].role == "unverified":
        user_roles[0].delete()
        Role.add_role_for_user(username=user_email, role="free")
        return {"message": f"User email verified for: {user_email}"}
    else:
        raise HTTPException(status_code=401, detail="User already verified")


@auth_router.post("/registration")
async def email_registration(request: Request):
    data = await request.json()
    user = User.get_user_by_email(email=data.get("email"))

    if not user:
        new_user = User(email=data.get("email"), password=data.get("password"))
        role = Role(username=new_user.email, role="unverified")
        verification_token = jwt.create_access_token(
            identity=new_user.email,
            additional_claims={"type": "registration"},
            expires_delta=timedelta(hours=24)
        )
        role.save()
        new_user.save()
        send_password_reset_email(new_user.email, verification_token)
        return {"message": "User created"}
    else:
        user_roles = Role.get_all_roles_for_user(username=user.email)
        if len(user_roles) == 1 and user_roles[0].role == "unverified":
            verification_token = jwt.create_access_token(
                identity=user.email,
                additional_claims={"type": "registration"},
                expires_delta=timedelta(hours=24)
            )
            send_password_reset_email(user.email, verification_token)
            return {"message": "User exists, resending verification email"}
        else:
            raise HTTPException(status_code=409, detail="User already verified")


@auth_router.post("/login")
async def login_user(request: Request, response: Response):
    data = await request.json()
    user = User.get_user_by_email(email=data.get("email"))

    if user and user.check_password(password=data.get("password")):
        roles_list = Role.get_all_roles_for_user(username=user.email)
        roles_list_str = [r.role for r in roles_list]

        access_token = jwt.create_access_token(identity=user.email, additional_claims={"roles": roles_list_str})
        refresh_token = jwt.create_refresh_token(identity=user.email)

        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
        return {"message": "Authentication successful", "access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@auth_router.get("/whoami")
async def whoami(current_user: str = Depends(jwt.get_current_user)):
    return {"message": {"user_details": {"email": current_user}}}


@auth_router.post("/register")
async def register_user(request: Request):
    data = await request.json()
    user = User.get_user_by_email(email=data.get("email"))

    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")
    
    # Create the user
    new_user = User(email=data.get("email"), password=data.get("password"))
    
    # Add the user as a free user
    Role.add_role_for_user(username=new_user.email, role="free")
    new_user.save()
    
    return {"message": "User created"}