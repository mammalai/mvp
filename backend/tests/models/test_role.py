import os
import pytest
from httpx import AsyncClient
from backend.models import Role
from backend.app import app
from backend.config import TestConfig

@pytest.fixture
async def client():
    """
    Fixture to provide an AsyncClient for testing FastAPI endpoints.
    """
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        if os.environ.get("DB_TYPE") == "mongodb":
            # Clean up the database before running the test
            db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
            yield test_client
            # Drop the database after running the test
            db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
        elif os.environ.get("DB_TYPE") == "sqlalchemy":
            with app.app_context():
                db.create_all()
                yield test_client
                db.drop_all()
        else:
            raise Exception("DB_TYPE not set in configuration.")


@pytest.mark.asyncio
async def test_create_role(client):
    """
    Test creating a role for a user.
    """
    # Arrange
    new_role = {"username": "ssatti", "role": "free"}

    # Act
    response = await client.post("/api/roles", json=new_role)

    # Assert
    assert response.status_code == 201
    role = Role.query.filter_by(username="ssatti").first()
    assert role is not None
    assert role.username == "ssatti"
    assert role.role == "free"


@pytest.mark.asyncio
async def test_delete_role(client):
    """
    Test deleting a role for a user.
    """
    # Arrange
    new_role = Role(username="ssatti", role="free")
    new_role.save()

    # Act
    response = await client.delete(f"/api/roles/{new_role.id}")

    # Assert
    assert response.status_code == 204
    role = Role.query.filter_by(username="ssatti", role="free").first()
    assert role is None


@pytest.mark.asyncio
async def test_get_all_roles_for_user(client):
    """
    Test retrieving all roles for a user.
    """
    # Arrange
    role1 = Role(username="ssatti", role="paid")
    role2 = Role(username="ssatti", role="staff")
    role1.save()
    role2.save()

    # Act
    response = await client.get("/api/roles?username=ssatti")

    # Assert
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) == 2
    roles_str = [r["role"] for r in roles]
    assert set(roles_str) == {"paid", "staff"}


@pytest.mark.asyncio
async def test_role_exists_for_user_true(client):
    """
    Test checking if a role exists for a user (true case).
    """
    # Arrange
    new_role = Role(username="ssatti", role="paid")
    new_role.save()

    # Act
    response = await client.get("/api/roles/exists", params={"username": "ssatti", "role": "paid"})

    # Assert
    assert response.status_code == 200
    assert response.json()["exists"] is True


@pytest.mark.asyncio
async def test_role_exists_for_user_false(client):
    """
    Test checking if a role exists for a user (false case).
    """
    # Act
    response = await client.get("/api/roles/exists", params={"username": "ssatti", "role": "paid"})

    # Assert
    assert response.status_code == 200
    assert response.json()["exists"] is False


@pytest.mark.asyncio
async def test_add_role_for_user(client):
    """
    Test adding a role for a user.
    """
    # Arrange
    username = "ssatti"
    role = "paid"

    # Act
    response = await client.post("/api/roles", json={"username": username, "role": role})

    # Assert
    assert response.status_code == 201
    r = Role.query.filter_by(username=username, role=role).first()
    assert r.username == username
    assert r.role == role


@pytest.mark.asyncio
async def test_remove_role_for_user(client):
    """
    Test removing a role for a user.
    """
    # Arrange
    username = "ssatti"
    role = "paid"
    new_role = Role(username=username, role=role)
    new_role.save()

    # Act
    response = await client.delete(f"/api/roles/{new_role.id}")

    # Assert
    assert response.status_code == 204
    r = Role.query.filter_by(username=username, role=role).first()
    assert r is None