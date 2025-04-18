import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.models import User
from backend.repositories.user import UsersRepository
from backend.helpers.utils import check_password_hash

@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(strong_password):
    """
    Test creating a user.
    """
    """
    arrange
    """
    test_email = "s@gmai.com"
    new_user = User(email=test_email, password=strong_password)
    """
    act
    """
    await UsersRepository.save(new_user)
    # Add assertions to verify that the user was created successfully
    user = await UsersRepository.get_user_by_email(test_email)
    """
    assert
    """
    assert user is not None
    assert user.email == test_email
    assert check_password_hash(user._password, strong_password)

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(strong_password):
    """
    Test deleting a user.
    """
    """
    arrange
    """
    test_email = "s@gmail.com"
    # set the new user, password, and save the user
    new_user = User(email="s@gmail.com", password=strong_password)
    await UsersRepository.save(new_user)
    """
    act
    """
    user = await UsersRepository.get_user_by_email(test_email)
    await UsersRepository.delete(user.id)
    """
    assert
    """
    user = await UsersRepository.get_user_by_email(test_email)
    assert user is None

@pytest.mark.asyncio(loop_scope="session")
async def test_update_with_weak_password(strong_password):
    """
    Test updating a user with a weak password.
    """
    """
    arrange
    """
    # set the new user
    new_user = User(email="s@gmai.com", password=strong_password)
    """
    assert
    """
    with pytest.raises(ValueError) as excinfo:
        new_user.password = f"short"
    assert "Password must be at least 8 characters long" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        new_user.password= f"no_upper_case"
    assert "Password must contain at least one uppercase letter" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        new_user.password = f"NO_LOWER_CASE"
    assert "Password must contain at least one lowercase letter" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        new_user.password = f"NO_numberS"
    assert "Password must contain at least one number" in str(excinfo.value)

    new_user.password = f"new_{strong_password}"

@pytest.mark.asyncio(loop_scope="session")
async def test_update_user_password(strong_password):
    """
    Test updating a user's password.
    """
    """
    arrange
    """
    test_email = "s@gmai.com"
    # set the new user
    new_user = User(email=test_email, password=f"old_{strong_password}")
    await UsersRepository.save(new_user)
    """
    act
    """
    user = await UsersRepository.get_user_by_email(test_email)
    user.password = f"new_{strong_password}"
    await UsersRepository.save(user)
    """
    assert
    """
    user = await UsersRepository.get_user_by_email(test_email)
    assert(user is not None)
    assert check_password_hash(user._password, f"new_{strong_password}")
