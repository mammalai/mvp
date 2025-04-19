import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.models import User
from backend.models.mongodb.role import Role, RoleName
from backend.repositories.user import UsersRepository
from datetime import timedelta
from backend.services.auth import AuthService
from backend.helpers.utils import generate_password_hash, check_password_hash

@pytest.mark.asyncio(loop_scope="session")
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
    user = await UsersRepository.get_user_by_email(email)
    assert user is not None
    assert user.email == email
    assert check_password_hash(user._password, strong_password)
    assert user.has_role(Role(RoleName.UNVERIFIED))

    # Act: Verify with an invalid token
    response = await client.post(f"/api/auth/verification?token=invalid_token")
    assert response.status_code == 400
    assert response.json()["detail"] == "Email verification failed"

    # Act: Verify with a valid token
    verification_token = AuthService.create_token(
        data={"sub": user.email, "type": "registration"},
        expires_delta=timedelta(seconds=10)
    )
    response = await client.post(f"/api/auth/verification?token={verification_token}")
    assert response.status_code == 201
    assert response.json()["message"] == "Email verification successful"

    # Assert: Verify role update
    user = await UsersRepository.get_user_by_email(email)
    assert user.has_role(Role(RoleName.FREE))

@pytest.mark.asyncio(loop_scope="session")
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


@pytest.mark.asyncio(loop_scope="session")
async def test_login_success(client, strong_password):
    """
    Test successful login with valid credentials.
    """
    # Arrange: Create a user
    new_user = User(email="test@gmail.com", password=strong_password)
    await UsersRepository.save(new_user)

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


@pytest.mark.asyncio(loop_scope="session")
async def test_reset_password_non_existent_user(client):
    """
    Test password reset request for a non-existent user.
    """
    response = await client.post("/api/auth/password/reset", json={
        "email": "nonexistent@email.com"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Password reset email sent"


@pytest.mark.asyncio(loop_scope="session")
async def test_reset_password(client, strong_password):
    """
    Test password reset with a valid token.
    """
    # Arrange: Create a user
    test_username = "reset_password_user"
    email = f"{test_username}@gmail.com"
    new_user = User(email=email, password=strong_password)
    new_user_password_hash = new_user._password
    await UsersRepository.save(new_user)

    # Act: Request password reset
    response = await client.post("/api/auth/password/reset", json={
        "email": email
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Password reset email sent"

    # Generate a valid reset token
    reset_token = AuthService.create_token(
        data={"sub": email, "type": "password_reset", "password_hash": generate_password_hash(new_user_password_hash[16:32])},
        expires_delta=timedelta(seconds=100)
    )

    # Act: Reset the password
    new_password = f"new_{strong_password}"
    response = await client.post(f"/api/auth/password?token={reset_token}", json={
        "password": new_password
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successful"

    # Assert: Verify the new password
    user = await UsersRepository.get_user_by_email(email)
    assert check_password_hash(user._password, new_password)


@pytest.mark.asyncio(loop_scope="session")
async def test_whoami(client, strong_password):
    """
    Test the /whoami endpoint with a valid access token.
    """
    # Arrange: Create a valid access token with roles
    identity = "testuser@gmail.com"
    access_token = AuthService.create_token(
        data={"sub": identity, "roles": ["free"]},  # Add roles like in the login endpoint
        expires_delta=timedelta(seconds=100)
    )

    new_user = User(email=identity, password=strong_password)
    await UsersRepository.save(new_user)
    
    # Act: Call the /whoami endpoint
    response = await client.get(
        "/api/auth/whoami", 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Assert: Verify the response
    assert response.status_code == 200
    assert response.json()["email"] == identity
