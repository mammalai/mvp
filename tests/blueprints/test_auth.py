import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from backend.app import create_app, db
from backend.models.user import User, EmailPasswordReset, EmailVerification
from backend.models.role import Role

@pytest.fixture
def client():
	app = create_app()
	#   app.testing = True
	with app.test_client() as testclient:
		with app.app_context():
			db.create_all()
			yield testclient

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
    response = client.post("/auth/emailregistration", json={
        "email": email,
        "password": strong_password
    })
    assert response.status_code == 201
    """
    assert
    """
    user = User.query.filter_by(email=email).first()
    assert user is not None
    assert user.email == email
    assert user.check_password(strong_password)
    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "unverified"

    email_verification = EmailVerification.get_email_verification_by_email(email=email)

    response = client.post(f"/auth/emailverification?token=invalid_token")
    assert response.status_code == 400
    assert response.json["error"] == "Invalid token"

    response = client.post(f"/auth/emailverification?token={email_verification.token}")
    assert response.status_code == 201
    assert response.json["message"] == f"User email verified for: {email_verification.email}"

    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "free"

def test_login_failure(client):
	response = client.post("/auth/login", json={
        "email": "mondragon@gmail.com",
        "password": "secret"
    })
	assert response.status_code == 400
	assert response.json["error"] == "Invalid username or password"
	
def test_login_success(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        test_username = "test_user"
        new_user = User(username=test_username, email="test@gmail.com")
        new_user.set_password(password=strong_password)
        """
        act
        """
        new_user.save()

    response = client.post("/auth/login", json={
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
    act
    """
    response = client.post("/auth/password-reset/request", json={
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
        new_user = User(username=test_username, email=email)
        new_user.set_password(password=strong_password)
        user_role = Role(username=email, role="unverified")
        
        new_user.save()
        user_role.save()

    """
    act
    """
    response = client.post("/auth/password-reset/request", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

    response = client.post("/auth/password-reset/password?token=non_existent_token", json={
        "password": f"new_{strong_password}"
    })
    
    """
    assert
    """
    assert response.status_code == 400
    assert response.json["error"] == "Invalid token"

def test_reset_password(client, strong_password):
    with client.application.app_context():
        """
		arrange
		"""
        test_username = "reset_password_user"
        email = f"{test_username}@gmail.com"
        new_user = User(username=test_username, email=email)
        new_user.set_password(password=strong_password)
        user_role = Role(username=email, role="unverified")
        
        new_user.save()
        user_role.save()

    """
    act
    """
    response = client.post("/auth/password-reset/request", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json["message"] == "Password reset email sent"

    epr = EmailPasswordReset.get_epr_by_email(email=email)

    response = client.post(f"/auth/password-reset/password?token={epr.token}", json={
        "password": f"new_{strong_password}"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Password reset successful"
    """
    assert
    """
