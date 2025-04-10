import pytest
from backend.models import Role
from backend.repositories.role import RolesRepository
from backend.services.role import RoleService

@pytest.mark.asyncio(loop_scope="session")
async def test_create_role():
    """
    Test creating a role for a user.
    """
    new_role = Role(username="ssatti", role="free")

    """
    act
    """
    await RolesRepository.save(new_role)
    # Add assertions to verify that the user was created successfully
    roles = await RolesRepository.get_all_roles_for_user(username="ssatti")
    role = roles[0]
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
    await RolesRepository.save(new_role)
    """
    act
    """
    role = await RolesRepository.get_by_id(new_role.id)
    await RolesRepository.delete(role.id)
    """
    assert
    """
    role = await RolesRepository.get_by_id(new_role.id)
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
    await RolesRepository.save(new_role1)
    new_role2 = Role(username="ssatti", role=role2)
    await RolesRepository.save(new_role2)
    """
    act
    """
    roles = await RolesRepository.get_all_roles_for_user("ssatti")
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
    await RolesRepository.save(new_role)
    """
    act
    """
    role_exists = await RoleService.role_exists_for_user("ssatti", role)
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
    role_exists = await RoleService.role_exists_for_user("ssatti", role)
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
    await RoleService.add_role_for_user(username=username, role=role)
    """
    assert
    """
    role_exists = await RoleService.role_exists_for_user("ssatti", role)
    assert role_exists == True


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
    await RolesRepository.save(new_role)
    """
    act
    """
    await RoleService.remove_role_for_user(username=username, role=role)
    """
    assert
    """
    role_exists = await RoleService.role_exists_for_user("ssatti", role)
    assert role_exists == False
