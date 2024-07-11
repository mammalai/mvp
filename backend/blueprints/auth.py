from flask import Blueprint, jsonify, request, make_response, current_app

from jwt import ExpiredSignatureError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
    decode_token
)


import sys
from backend.models.user import User
from backend.models.token import TokenBlocklist 
from backend.models.role import Role

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import uuid
import os

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/password")
def password_reset_new_password():
    """
        Update the user's password with a new password
    """
    reset_token = request.args.get("token")
    data = request.get_json()
    # check if the token is expired
    try:
        # decode the token
        decoded_token = decode_token(reset_token) # if the token is expired, this will raise an exception
    except Exception as e:
        if (type(e) == ExpiredSignatureError):
            return jsonify({"error": "Token has expired"}), 401
        else:
            return jsonify({"error": "Invalid token"}), 401
    # check if the token is of the correct type
    # make sure the token is of registration token - no other token types are allowed
    if decoded_token["type"] != "password_reset": #TO DO: move logic to decorator
        return jsonify({"error": "Not a registration token"}), 401
    # get the user email from the decoded token
    user_email = decoded_token['sub']

    user = User.get_user_by_email(email=user_email)

    if user is None:
        return jsonify({"error": "Invalid token"}), 400
    else:
        # check if the partial password hash is the same as the old partial password
        if check_password_hash(decoded_token['password_hash'], user._password[16:32]):
            # set the new password
            user.password = data.get("new_password")
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"error": "Invalid token"}), 400        
    
def send_password_reset_email(email, reset_token):
    print(f"Sending password reset email to {email}")

    # if we are in test mode, do not send the email
    if os.environ.get("FLASK_ENV") == "TEST" or os.environ.get("FLASK_ENV") == None:
        return
    
    message = Mail(
        from_email=f'info@{os.environ.get("DOMAIN_NAME")}',
        to_emails=email,
        subject=f'{os.environ.get("DOMAIN_NAME")} - Password reset',
        html_content=
            f"""
                <strong>
                    Your sent a password reset request to {email}.
                </strong>
                <br>
                <br>
                <a href="{current_app.config['FRONT_END_URL']}/password-reset/password?token={reset_token}">Click here to reset your password</a>
                <p>{reset_token}</p>
            """
    )
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if sendgrid_api_key:
        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
            raise Exception("Error sending email") from e
    else:
        raise Exception("No sendgrid API key found")
    
@auth_bp.post("/password/reset")
def password_reset_request_email():
    """
        Send a password reset email to the user
    """
    data = request.get_json()
    email = data.get("email")
    print(f"Password reset request for email: {email}")

    user = User.get_user_by_email(email=email)
    # If the user is not found, do not reveal this to the client by sending
    # a 400 response. If we send a 400 response, an attacker could use this
    # to determine if an email is registered with our service.
    if user is None:
        return jsonify({"message": "Password reset email sent"}), 201
    else:
        verification_token = create_access_token(
            identity=user.email, # user email as the identity
            additional_claims={"type": "password_reset", "password_hash":generate_password_hash(user._password[16:32])}, # type referes to the token type
            expires_delta=current_app.config["JWT_PASSWORD_TOKEN_EXPIRES"] # how long before a token expires
        )
        send_password_reset_email(user.email, verification_token)
        return jsonify({"message": "Password reset email sent"}), 201

@auth_bp.post("/justjwt")
def test_jwt():
    verification_token = request.args.get("token")
    print(f"Verification token: {verification_token}")
    decoded_token = decode_token(verification_token) # decode_token returns the decoded token (python dict) from an encoded JWT.
    
    try:
        decoded_token = decode_token(verification_token)
        jsonify({"message": "User email verified"}), 200
    except Exception as e:
        if (type(e) == ExpiredSignatureError):
            return jsonify({"error": "Token expired"}), 400
        else:
            raise e


    print(decoded_token)
    return jsonify({"message": "Token decoded bruh"}), 200

@auth_bp.post("/verification")
def email_verification():
    """
        This endpoint will allow a user to verify their email address but will allow multiple 
        authentication tokens to be active.
    """
    # get the token from the URL query string
    verification_token = request.args.get("token")

    try:
        # decode the token
        decoded_token = decode_token(verification_token) # if the token is expired, this will raise an exception
    except Exception as e:
        if (type(e) == ExpiredSignatureError):
            return jsonify({"error": "Token has expired"}), 401
        else:
            return jsonify({"error": "Invalid token"}), 401
    # make sure the token is of registration token - no other token types are allowed
    if decoded_token["type"] != "registration": #TO DO: move logic to decorator
        return jsonify({"error": "Not a registration token"}), 401
    # get the user email from the decoded token
    user_email = decoded_token['sub']
    # delete any roles that are labelled as unverified
    user_roles = Role.get_all_roles_for_user(username=user_email)
    if (len(user_roles)) == 1 and (user_roles[0].role == 'unverified'): # there should only be one role called unverified
        user_roles[0].delete()
        # add the user as a free user
        Role.add_role_for_user(username=user_email, role='free')
        return jsonify({"message": f"User email verified for: {user_email}"}), 201
    else:
        return jsonify({"error": "User already verified"}), 401


def send_email_verification_email(email, verification_token):
    print(f"Sending email verification email to {email}")

    if os.environ.get("FLASK_ENV") == "TEST" or os.environ.get("FLASK_ENV") == None:
        return

    message = Mail(
        from_email=f'info@{os.environ.get("DOMAIN_NAME")}',
        to_emails=email,
        subject=f'{os.environ.get("DOMAIN_NAME")} - Account verification',
        html_content=
            f"""
                <strong>
                    Please verify yout email: {email}
                </strong>
                <br>
                <br>
                <a href="{current_app.config['FRONT_END_URL']}/register-verify?token={verification_token}">Click here to verify your email</a>
                <p>{verification_token}</p>
            """
    )
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if sendgrid_api_key:
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
            raise Exception("Error sending email") from e
    else:
        raise Exception("No sendgrid API key found")

@auth_bp.post("/registration")
def email_registration():
    data = request.get_json()

    # check the database for the user
    user = User.get_user_by_email(email=data.get("email"))
    # if the user does not exist
    if user is None:
        # create the user
        new_user = User(email=data.get("email"), password=data.get("password"))
        # add the user role to be an unverified user
        role = Role(username=new_user.email, role='unverified')
        # create a JWT access token
        verification_token = create_access_token(
            identity=new_user.email, # user email as the identity
            additional_claims={"type": "registration"}, # type referes to the token type
            expires_delta=current_app.config["JWT_REGISTRATION_TOKEN_EXPIRES"] # how long before a token expires
        )
        # commit everything to the database and send the email
        role.save()
        new_user.save()
        send_email_verification_email(new_user.email, verification_token)
        return jsonify({"message": "User created"}), 201
    # if the user exists
    else:
        # check the roles in the database
        user_roles = Role.get_all_roles_for_user(username=user.email)
        # if there is one role and that role is unverified, create a new token and resend the verification email
        if (len(user_roles)) == 1 and (user_roles[0] == 'unverified'):
            # create a JWT access token
            verification_token = create_access_token(
                identity=new_user.email, # user email as the identity
                additional_claims={"type": "registration"}, # type referes to the token type
                expires_delta=current_app.config["JWT_REGISTRATION_TOKEN_EXPIRES"] # how long before a token expires
            )
            # resend the verification email
            send_email_verification_email(new_user.email, verification_token)
            return jsonify({"message": "User exists, resending verificaiton email"}), 200
        # if there are other roles apart from unverified the user is already verified
        else:  
            return jsonify({"error": "User already verified"}), 409
   


@auth_bp.post("/register")
def register_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409
    # create the user
    new_user = User(email=data.get("email"), password=data.get("password"))
    new_user.save()
    # add the user as a free user
    Role.add_role_for_user(username=new_user.email, role='free')

    return jsonify({"message": "User created"}), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_email(email=data.get("email"))

    if user and (user.check_password(password=data.get("password"))):
        roles_list = Role.get_all_roles_for_user(username=user.email)
        roles_list_str = [r.role for r in roles_list]
        
        access_token = create_access_token(identity=user.email, additional_claims={"roles": roles_list_str})
        refresh_token = create_refresh_token(identity=user.email)

        response = make_response(
            jsonify({
                "message": "Authentication successful",
                "access_token": access_token
            }), 200
        )

        # HTTP-only cookies cannot be accessed via JavaScript which prevents client-side scripts
        # from reading the token.
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
        return response
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "email": current_user.email,
            },
        }
    )

@auth_bp.get("/refresh")
@jwt_required(refresh=True) # refresh – If True, requires a refresh JWT to access this endpoint. If False, requires an access JWT to access this endpoint. Defaults to False.
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})


@auth_bp.get('/logout')
@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)
    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}) , 200