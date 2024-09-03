import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.app import create_app, db
from backend.models import User

@pytest.fixture
def client():
	app = create_app()
	#   app.testing = True
	# with app.test_client() as testclient:
	# 	with app.app_context():
	# 		db.create_all()
	# 		yield testclient
	with app.test_client() as testclient:
		yield testclient

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
		user = User.query.filter_by(email=test_email).first()
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
		user = User.query.filter_by(email=test_email).first()
		new_user.delete()
		"""
		assert
		"""
		user = User.query.filter_by(email=test_email).first()
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
		user = User.query.filter_by(email=test_email).first()
		user.password = f"new_{strong_password}"
		user.save()
		"""
		assert
		"""
		user = User.query.filter_by(email=test_email).all()
		assert(len(user) == 1)
		assert user[0].check_password(f"new_{strong_password}")