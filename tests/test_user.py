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

def test_create_user(client):
	with client.application.app_context():
		"""
		arrange
		"""
		test_username = "ssatti"
		new_user = User(username=test_username, email="s@gmai.com")
		new_user.set_password(password="1234")
		"""
		act
		"""
		new_user.save()
		# Add assertions to verify that the user was created successfully
		user = User.query.filter_by(username=test_username).first()
		"""
		assert
		"""
		assert user is not None
		assert user.username == test_username
		assert user.check_password("1234")

def test_delete_user(client):
	with client.application.app_context():
		"""
		arrange
		"""
		test_username = "ssatti"
		# set the new user, password, and save the user
		new_user = User(username=test_username, email="s@gmail.com")
		new_user.set_password(password="1234")
		new_user.save()
		"""
		act
		"""
		user = User.query.filter_by(username=test_username).first()
		new_user.delete()
		"""
		assert
		"""
		user = User.query.filter_by(username=test_username).first()
		assert user is None

def test_update_user_password(client):
	with client.application.app_context():
		"""
		arrange
		"""
		test_username = "ssatti"
		# set the new user
		new_user = User(username=test_username, email="s@gmai.com")
		new_user.set_password(password="old_password")
		new_user.save()
		"""
		act
		"""
		user = User.query.filter_by(username=test_username).first()
		user.set_password(password="new_password")
		user.save()
		"""
		assert
		"""
		user = User.query.filter_by(username=test_username).all()
		assert(len(user) == 1)
		assert user[0].check_password("new_password")