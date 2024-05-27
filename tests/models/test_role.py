import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from backend.app import create_app, db
from backend.models.role import Role

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
		
		new_role = Role(username="ssatti", role="free")
		"""
		act
		"""
		new_role.save()
		# Add assertions to verify that the user was created successfully
		role = Role.query.filter_by(username="ssatti").first()
		"""
		assert
		"""
		assert role is not None
		assert role.username == "ssatti"
		assert role.role == "free"