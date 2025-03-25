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

from httpx import AsyncClient
from backend.app import app
from backend.models import User, Role
from backend.config import TestConfig
from werkzeug.security import generate_password_hash

@pytest.fixture
async def client():
    """
    Fixture to provide an AsyncClient for testing FastAPI endpoints.
    """
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
def strong_password():
    return "StrongPassword123"


@pytest.mark.asyncio
async def test_register_with_verification(client, strong_password):
    """
    Test user registration with email verification.
    """
    test_username = "register_test_user"
    email = f"{test_username}@gmail.com"

    # Act: Register the user
    response = await client.post("/api/auth/registration", json={
        "email": email,
        "password": strong_password
    })
    assert response.status_code == 201

    # Assert: Verify user creation
    user = User.get_user_by_email(email)
    assert user is not None
    assert user.email == email
    assert user.check_password(strong_password)
    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "unverified"

    # Act: Verify with an invalid token
    response = await client.post(f"/api/auth/verification?token=invalid_token")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

    # Act: Verify with a valid token
    verification_token = app.jwt.create_access_token(
        identity=user.email,
        additional_claims={"type": "registration"}
    )
    response = await client.post(f"/api/auth/verification?token={verification_token}")
    assert response.status_code == 201
    assert response.json()["message"] == f"User email verified for: {user.email}"

    # Assert: Verify role update
    roles_list = Role.get_all_roles_for_user(username=user.email)
    assert roles_list[0].role == "free"


@pytest.mark.asyncio
async def test_login_failure(client):
    """
    Test login failure with invalid credentials.
    """
    response = await client.post("/api/auth/login", json={
        "email": "nonexistent@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_success(client, strong_password):
    """
    Test successful login with valid credentials.
    """
    # Arrange: Create a user
    new_user = User(email="test@gmail.com", password=strong_password)
    new_user.save()

    # Act: Login with valid credentials
    response = await client.post("/api/auth/login", json={
        "email": "test@gmail.com",
        "password": strong_password
    })

    # Assert: Verify response
    assert response.status_code == 200
    assert response.json()["message"] == "Authentication successful"
    assert "access_token" in response.json()

    # Assert: Verify refresh token in cookies
    cookies = response.cookies
    assert "refresh_token" in cookies


@pytest.mark.asyncio
async def test_reset_password_non_existent_user(client):
    """
    Test password reset request for a non-existent user.
    """
    response = await client.post("/api/auth/password/reset", json={
        "email": "nonexistent@email.com"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Password reset email sent"


@pytest.mark.asyncio
async def test_reset_password(client, strong_password):
    """
    Test password reset with a valid token.
    """
    # Arrange: Create a user
    test_username = "reset_password_user"
    email = f"{test_username}@gmail.com"
    new_user = User(email=email, password=strong_password)
    new_user.save()

    # Act: Request password reset
    response = await client.post("/api/auth/password/reset", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Password reset email sent"

    # Generate a valid reset token
    reset_token = app.jwt.create_access_token(
        identity=email,
        additional_claims={"type": "password_reset"}
    )

    # Act: Reset the password
    new_password = f"new_{strong_password}"
    response = await client.post(f"/api/auth/password?token={reset_token}", json={
        "password": new_password
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successful"

    # Assert: Verify the new password
    user = User.get_user_by_email(email)
    assert user.check_password(new_password)


@pytest.mark.asyncio
async def test_whoami(client):
    """
    Test the /whoami endpoint with a valid access token.
    """
    # Arrange: Create a valid access token
    identity = "testuser@gmail.com"
    access_token = app.jwt.create_access_token(identity=identity)

    # Act: Call the /whoami endpoint
    response = await client.get("/api/auth/whoami", headers={
        "Authorization": f"Bearer {access_token}"
    })

    # Assert: Verify the response
    assert response.status_code == 200
    assert response.json()["message"]["user_details"]["email"] == identity
