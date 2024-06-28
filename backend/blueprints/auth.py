from flask import Blueprint, jsonify, request, make_response, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)

import sys
from backend.models.user import User
from backend.models.token import TokenBlocklist 
from backend.models.role import Role
from backend.models.user import EmailVerification
from backend.models.user import EmailPasswordReset

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import uuid
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/password")
def password_reset_new_password():
    reset_token = request.args.get("token")
    data = request.get_json()
    # use the token to get the email/user password reset
    epr = EmailPasswordReset.get_epr_by_token(token=reset_token)

    if epr is None:
        return jsonify({"error": "Invalid token"}), 400
    else:
        # update the user's password from the data in the dictionary
        u = User.get_user_by_email(email=epr.email)
        u.password = data.get("password")
        u.save()
        # delete the token so it can't be used again
        epr.delete()
        return jsonify({"message": "Password reset successful"}), 200
    
def send_password_reset_email(email, reset_token):
    print(f"Sending password reset email to {email}")
    
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
        token = str(uuid.uuid4())
        # remove any old password reset tokens
        old_epr = EmailPasswordReset.get_epr_by_email(email=user.email)
        if old_epr is not None:
            old_epr.delete()
        # create a new password reset token
        new_reset = EmailPasswordReset(email=user.email, token=token)
        send_password_reset_email(user.email, token)
        new_reset.save() # only save the reset token if the email was sent
        return jsonify({"message": "Password reset email sent"}), 201


@auth_bp.post("/verification")
def email_verification():
    verification_token = request.args.get("token")

    email_verification = EmailVerification.get_email_verification_by_token(token=verification_token)
    if email_verification is None:
        return jsonify({"error": "Invalid token"}), 400
    else:
        # delete any roles that are labelled as unverified
        user_roles = Role.get_all_roles_for_user(username=email_verification.email)
        user_roles[0].delete()

        # add the user as a free user
        Role.add_role_for_user(username=email_verification.email, role='free')
        email_verification.delete()
        return jsonify({"message": f"User email verified for: {email_verification.email}"}), 201


def send_email_verification_email(email, verification_token):
    print(f"Sending email verification email to {email}")
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
    user = User.get_user_by_email(email=data.get("email"))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409
    # create the user
    new_user = User(email=data.get("email"), password=data.get("password"))
    # add the user as a free user
    role = Role(username=new_user.email, role='unverified')
    
    verification_token = str(uuid.uuid4())
    new_verification = EmailVerification(email=new_user.email, token=verification_token)
    
    role.save()
    new_user.save()
    new_verification.save()

    send_email_verification_email(new_user.email, verification_token)

    return jsonify({"message": "User created"}), 201


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
@jwt_required(refresh=True)
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