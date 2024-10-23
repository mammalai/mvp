import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.app import create_app, db
from backend.models import User
from backend.models import Role

import time
from flask import current_app
from flask_jwt_extended import create_access_token
from backend.config import TestConfig

from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def client():
	app = create_app()
	
	if os.environ.get("DB_TYPE") == "mongodb":
		with app.test_client() as testclient:
			with app.app_context():
				# clean up the database after running the test
				db.cx.drop_database(f'{TestConfig.project_name}')
				yield testclient
	elif os.environ.get("DB_TYPE") == "sqlalchemy":
		with app.test_client() as testclient:
			with app.app_context():
				db.create_all()
				yield testclient
	else:
		raise Exception("DB_TYPE not set in configuration.")
    

@pytest.fixture
def strong_password():
    return "StrongPassword123"

def test_register_with_verification(client, strong_password):
    """
    arrange
    """
    test_username = "register_test_user"
    email = f"{test_username}@gmail.com"
    """
    act
    """
    response = client.post("/api/auth/registration", json={
        "email": email,
        "password": strong_password
    })
    assert response.status_code == 201
    """
    assert
    """
    user = User.get_user_by_email(email)
    assert user is not None
    assert user.email == email
    assert user.check_password(strong_password)
    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "unverified"

    response = client.post(f"/api/auth/verification?token=invalid_token")
    assert response.status_code == 401
    assert response.json["error"] == "Invalid token"

    verification_token = create_access_token(
        identity=user.email, # user email as the identity
        additional_claims={"type": "registration"}, # type referes to the token type
        expires_delta=current_app.config["JWT_REGISTRATION_TOKEN_EXPIRES"] # how long before a token expires
    )

    response = client.post(f"/api/auth/verification?token={verification_token}")
    assert response.status_code == 201
    assert response.json["message"] == f"User email verified for: {user.email}"

    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "free"

def test_register_with_verification_expired_token(client, strong_password):
    """
    arrange
    """
    test_username = "register_test_user"
    email = f"{test_username}@gmail.com"
    """
    act
    """
    response = client.post("/api/auth/registration", json={
        "email": email,
        "password": strong_password
    })
    assert response.status_code == 201
    """
    assert
    """
    user = User.get_user_by_email(email)
    assert user is not None
    assert user.email == email
    assert user.check_password(strong_password)
    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "unverified"

    verification_token = create_access_token(
        identity=user.email, # user email as the identity
        additional_claims={"type": "registration"}, # type referes to the token type
        expires_delta=current_app.config["JWT_REGISTRATION_TOKEN_EXPIRES"] # how long before a token expires
    )
     
    time.sleep(current_app.config['JWT_REGISTRATION_TOKEN_EXPIRES'].seconds+2)
    response = client.post(f"/api/auth/verification?token={verification_token}")
    assert response.status_code == 401
    assert response.json["error"] == "Token has expired"

def test_login_failure(client):
	response = client.post("/api/auth/login", json={
        "email": "mondragon@gmail.com",
        "password": "secret"
    })
	assert response.status_code == 401
	assert response.json["error"] == "Invalid username or password"
	
def test_login_success(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        new_user = User(email="test@gmail.com", password=strong_password)
        """
        act
        """
        new_user.save()

    response = client.post("/api/auth/login", json={
        "email": "test@gmail.com",
        "password": strong_password
    })
    """
    assert
    """
    assert response.status_code == 200
    assert response.json["message"] == "Authentication successful"
    assert "access_token" in response.json
    assert "refresh_token" not in response.json

    # Assert that "refresh_token" is in the Set-Cookie header
    assert "Set-Cookie" in response.headers
    cookies = response.headers.getlist("Set-Cookie")
    auth_cookie = next((cookie for cookie in cookies if cookie.startswith("refresh_token=")), None)

    assert auth_cookie is not None
    assert "HttpOnly" in auth_cookie
	
def test_reset_password_non_existent_user(client):
    """
    We want to do this so it is not easy for an attacker to know if a user exists in the system
    """
    """
    act
    """
    response = client.post("/api/auth/password/reset", json={
        "email": "non_existent@email.com"
    })
    """
    assert
    """
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

def test_reset_password_wrong_token(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        test_username = "wrong_reset_password_token"
        email = f"{test_username}@gmail.com"
        new_user = User(email=email, password=strong_password)
        user_role = Role(username=email, role="unverified")
        
        new_user.save()
        user_role.save()

    """
    act
    """
    response = client.post("/api/auth/password/reset", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

    response = client.post("/api/auth/password?token=non_existent_token", json={
        "password": f"new_{strong_password}"
    })
    
    """
    assert
    """
    assert response.status_code == 401
    assert response.json["error"] == "Invalid token"

def test_reset_password_expiration(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        test_username = "reset_password_user"
        email = f"{test_username}@gmail.com"
        new_user = User(email=email, password=strong_password)
        new_user_password_hash = new_user._password
        user_role = Role(username=email, role="unverified")
        
        new_user.save()
        user_role.save()

    """
    act
    """
    response = client.post("/api/auth/password/reset", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

    verification_token = create_access_token(
        identity=email, # user email as the identity
        additional_claims={"type": "password_reset", "password_hash":generate_password_hash(new_user_password_hash[16:32])}, # type referes to the token type
        expires_delta=current_app.config["JWT_PASSWORD_TOKEN_EXPIRES"] # how long before a token expires
    )
    time.sleep(current_app.config['JWT_PASSWORD_TOKEN_EXPIRES'].seconds+2)

    response = client.post(f"/api/auth/password?token={verification_token}", json={
        "password": f"new_{strong_password}"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Token has expired"
    """
    assert
    """

def test_reset_password(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        test_username = "reset_password_user"
        email = f"{test_username}@gmail.com"
        new_user = User(email=email, password=strong_password)
        new_user_password_hash = new_user._password
        user_role = Role(username=email, role="unverified")
        
        new_user.save()
        user_role.save()

    """
    act
    """
    response = client.post("/api/auth/password/reset", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

    verification_token = create_access_token(
        identity=email, # user email as the identity
        additional_claims={"type": "password_reset", "password_hash":generate_password_hash(new_user_password_hash[16:32])}, # type referes to the token type
        expires_delta=current_app.config["JWT_PASSWORD_TOKEN_EXPIRES"] # how long before a token expires
    )

    """
    assert
    """
    response = client.post(f"/api/auth/password?token={verification_token}", json={
        "password": f"new_{strong_password}"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Password reset successful"

    user = User.get_user_by_email(email)
    assert user.check_password(f"new_{strong_password}")

def test_whoami(client):
    """
    arrange
    """
    identity = "salarsattiss@gmail.com"
    new_access_token = create_access_token(identity=identity)

    headers={"Authorization": f"Bearer {new_access_token}"}
    """
    act
    """
    response = client.get("/api/auth/whoami", headers=headers)
    """
    assert
    """
    assert(response.status_code == 200)
    assert(response.json["message"]["user_details"]["email"] == identity)
