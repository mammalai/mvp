from flask import Blueprint, jsonify, request
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

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409
    # get the initial user
    new_user = User(username=data.get("username"), email=data.get("email"))
    # set the password hash
    new_user.set_password(password=data.get("password"))
    # commit the user to the database
    new_user.save()
    # add the user as a free user
    Role.add_role_for_user(username=new_user.username, role='free')

    return jsonify({"message": "User created"}), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(password=data.get("password"))):
             
        roles_list = Role.get_all_roles_for_user(username=user.username)
        
        access_token = create_access_token(identity=user.username, additional_claims={"roles": roles_list})
        refresh_token = create_refresh_token(identity=user.username)

        return (
            jsonify(
                {
                    "message": "Logged In ",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 400


@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "username": current_user.username,
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