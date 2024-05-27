import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from backend.app import create_app, db
from backend.models.user import User

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
