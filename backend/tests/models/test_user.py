import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.app import create_app, db
from backend.models import User
from backend.config import TestConfig

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

def test_create_user(client, strong_password):
	with client.application.app_context():
		"""
		arrange
		"""
		test_email = "s@gmai.com"
		new_user = User(email=test_email, password=strong_password)
		"""
		act
		"""
		new_user.save()
		# Add assertions to verify that the user was created successfully
		user = User.get_user_by_email(test_email)
		"""
		assert
		"""
		assert user is not None
		assert user.email == test_email
		assert user.check_password(strong_password)

def test_delete_user(client, strong_password):
	with client.application.app_context():
		"""
		arrange
		"""
		test_email = "s@gmail.com"
		# set the new user, password, and save the user
		new_user = User(email="s@gmail.com", password=strong_password)
		new_user.save()
		"""
		act
		"""
		user = User.get_user_by_email(test_email)
		new_user.delete()
		"""
		assert
		"""
		user = User.get_user_by_email(test_email)
		assert user is None

def test_update_with_weak_password(client, strong_password):
	with client.application.app_context():
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

def test_update_user_password(client, strong_password):
	with client.application.app_context():
		"""
		arrange
		"""
		test_email = "s@gmai.com"
		# set the new user
		new_user = User(email=test_email, password=f"old_{strong_password}")
		new_user.save()
		"""
		act
		"""
		user = User.get_user_by_email(test_email)
		user.password = f"new_{strong_password}"
		user.save()
		"""
		assert
		"""
		user = User.get_user_by_email(test_email)
		assert(user is not None)
		assert user.check_password(f"new_{strong_password}")