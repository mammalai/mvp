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

def test_create_role(client):
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
		
def test_delete_role(client):
	with client.application.app_context():
		"""
		arrange
		"""
		# set the new user, password, and save the user
		new_role = Role(username="ssatti", role="free")
		new_role.save()
		"""
		act
		"""
		role = Role.query.filter_by(username="ssatti", role="free").first()
		new_role.delete()
		"""
		assert
		"""
		role = Role.query.filter_by(username="ssatti", role="free").first()
		assert role is None
		
def test_get_all_roles_for_user(client):
	with client.application.app_context():
		"""
		arrange
		"""
		role1 = "paid"
		role2 = "staff"
		new_role1 = Role(username="ssatti", role=role1)
		new_role1.save()
		new_role2 = Role(username="ssatti", role=role2)
		new_role2.save()
		"""
		act
		"""
		roles = Role.get_all_roles_for_user("ssatti")
		"""
		assert
		"""
		assert len(roles) == 2
		roles_str = [r.role for r in roles]
		assert set(roles_str) == set([role1, role2])

def test_role_exists_for_user_true(client):
	with client.application.app_context():
		"""
		arrange
		"""
		role = "paid"
		new_role = Role(username="ssatti", role=role)
		new_role.save()
		"""
		act
		"""
		role_exists = Role.role_exists_for_user("ssatti", role)
		"""
		assert
		"""
		assert role_exists == True

def test_role_exists_for_user_false(client):
	with client.application.app_context():
		"""
		arrange
		"""
		role = "paid"
		"""
		act
		"""
		role_exists = Role.role_exists_for_user("ssatti", role)
		"""
		assert
		"""
		assert role_exists == False

def test_add_role_for_user(client):
	with client.application.app_context():
		"""
		arrange
		"""
		username = "ssatti"
		role = "paid"
		"""
		act
		"""
		Role.add_role_for_user(username=username, role=role)
		"""
		assert
		"""
		r = Role.query.filter_by(username=username, role=role).first()
		assert r.username == username
		assert r.role == role

def test_remove_role_for_user(client):
	with client.application.app_context():
		"""
		arrange
		"""
		username = "ssatti"
		role = "paid"
		new_role = Role(username=username, role=role)
		new_role.save()
		"""
		act
		"""
		Role.remove_role_for_user(username=username, role=role)
		"""
		assert
		"""
		r = Role.query.filter_by(username=username, role=role).first()
		assert r is None