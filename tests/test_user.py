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
			test_username = "ssatti"
			# set the new user
			new_user = User(username=test_username, email="s@gmai.com")
			# set the password hash
			new_user.set_password(password="1234")
			# commit the user to the database
			new_user.save()

			# Add assertions to verify that the user was created successfully
			user = User.query.filter_by(username=test_username).first()
			assert user is not None
			assert user.username == test_username
			assert user.check_password("1234")
