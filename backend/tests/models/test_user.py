import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from httpx import AsyncClient
from backend.app import create_app, db
from backend.models import User
from backend.config import TestConfig

@pytest.fixture
async def client():
    """
    Fixture to provide an AsyncClient for testing FastAPI endpoints.
    """
    async with AsyncClient(base_url="http://test") as test_client:
        if os.environ.get("DB_TYPE") == "mongodb":
            # Clean up the database before running the test
            db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
            yield test_client
            # Drop the database after running the test
            db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
        elif os.environ.get("DB_TYPE") == "sqlalchemy":
            db.create_all()
            yield test_client
            db.drop_all()
        else:
            raise Exception("DB_TYPE not set in configuration.")

@pytest.fixture
def strong_password():
    return "StrongPassword123"

@pytest.mark.asyncio
async def test_create_user(client, strong_password):
    """
    Test creating a user.
    """
    # Arrange
    test_email = "s@gmai.com"
    new_user = {"email": test_email, "password": strong_password}

    # Act
    response = await client.post("/api/users", json=new_user)

    # Assert
    assert response.status_code == 201
    user = User.get_user_by_email(test_email)
    assert user is not None
    assert user.email == test_email
    assert user.check_password(strong_password)

@pytest.mark.asyncio
async def test_delete_user(client, strong_password):
    """
    Test deleting a user.
    """
    # Arrange
    test_email = "s@gmail.com"
    new_user = User(email=test_email, password=strong_password)
    new_user.save()

    # Act
    response = await client.delete(f"/api/users/{new_user.id}")

    # Assert
    assert response.status_code == 204
    user = User.get_user_by_email(test_email)
    assert user is None

@pytest.mark.asyncio
async def test_update_with_weak_password(client, strong_password):
    """
    Test updating a user with a weak password.
    """
    # Arrange
    new_user = User(email="s@gmai.com", password=strong_password)
    new_user.save()

    # Act & Assert
    weak_passwords = [
        ("short", "Password must be at least 8 characters long"),
        ("no_upper_case", "Password must contain at least one uppercase letter"),
        ("NO_LOWER_CASE", "Password must contain at least one lowercase letter"),
        ("NO_numberS", "Password must contain at least one number"),
    ]

    for weak_password, error_message in weak_passwords:
        response = await client.put(f"/api/users/{new_user.id}/password", json={"password": weak_password})
        assert response.status_code == 400
        assert error_message in response.json()["detail"]

    # Act: Update with a strong password
    response = await client.put(f"/api/users/{new_user.id}/password", json={"password": f"new_{strong_password}"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_user_password(client, strong_password):
    """
    Test updating a user's password.
    """
    # Arrange
    test_email = "s@gmai.com"
    new_user = User(email=test_email, password=f"old_{strong_password}")
    new_user.save()

    # Act
    response = await client.put(f"/api/users/{new_user.id}/password", json={"password": f"new_{strong_password}"})

    # Assert
    assert response.status_code == 200
    user = User.get_user_by_email(test_email)
    assert user is not None
    assert user.check_password(f"new_{strong_password}")