import os
import pytest
from backend.models import Role
from backend.app import app
from backend.config import TestConfig

@pytest.mark.asyncio(loop_scope="session")
async def test_create_role():
    """
    Test creating a role for a user.
    """

    new_role = Role(username="ssatti", role="free")

    """
    act
    """
    await new_role.save()
    # Add assertions to verify that the user was created successfully
    roles = await Role.query.filter_by(username="ssatti")
    role = await roles.first()
    """
    assert
    """
    assert role is not None
    assert role.username == "ssatti"
    assert role.role == "free"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_role():
    """
    Test deleting a role for a user.
    """
    """
    arrange
    """
    # set the new user, password, and save the user
    new_role = Role(username="ssatti", role="free")
    await new_role.save()
    """
    act
    """
    roles = await Role.query.filter_by(username="ssatti", role="free")
    role = await roles.first()
    await new_role.delete()
    """
    assert
    """
    roles = await Role.query.filter_by(username="ssatti", role="free")
    role = await roles.first()
    assert role is None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_for_user():
    """
    Test retrieving all roles for a user.
    """
    """
    arrange
    """
    role1 = "paid"
    role2 = "staff"
    new_role1 = Role(username="ssatti", role=role1)
    await new_role1.save()
    new_role2 = Role(username="ssatti", role=role2)
    await new_role2.save()
    """
    act
    """
    roles = await Role.get_all_roles_for_user("ssatti")
    """
    assert
    """
    assert len(roles) == 2
    roles_str = [r.role for r in roles]
    assert set(roles_str) == set([role1, role2])


@pytest.mark.asyncio(loop_scope="session")
async def test_role_exists_for_user_true():
    """
    Test checking if a role exists for a user (true case).
    """
    """
    arrange
    """
    role = "paid"
    new_role = Role(username="ssatti", role=role)
    await new_role.save()
    """
    act
    """
    role_exists = await Role.role_exists_for_user("ssatti", role)
    """
    assert
    """
    assert role_exists == True


@pytest.mark.asyncio(loop_scope="session")
async def test_role_exists_for_user_false():
    """
    Test checking if a role exists for a user (false case).
    """
    """
    arrange
    """
    role = "paid"
    """
    act
    """
    role_exists = await Role.role_exists_for_user("ssatti", role)
    """
    assert
    """
    assert role_exists == False


@pytest.mark.asyncio(loop_scope="session")
async def test_add_role_for_user():
    """
    Test adding a role for a user.
    """
    """
    arrange
    """
    username = "ssatti"
    role = "paid"
    """
    act
    """
    await Role.add_role_for_user(username=username, role=role)
    """
    assert
    """
    roles = await Role.query.filter_by(username=username, role=role)
    r = await roles.first()
    assert r.username == username
    assert r.role == role


@pytest.mark.asyncio(loop_scope="session")
async def test_remove_role_for_user():
    """
    Test removing a role for a user.
    """
    """
    arrange
    """
    username = "ssatti"
    role = "paid"
    new_role = Role(username=username, role=role)
    await new_role.save()
    """
    act
    """
    await Role.remove_role_for_user(username=username, role=role)
    """
    assert
    """
    roles = await Role.query.filter_by(username=username, role=role)
    r = await roles.first()
    assert r is None
