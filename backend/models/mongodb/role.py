from uuid import uuid4
from datetime import datetime

from dataclasses import dataclass, field

from backend.extensions import db
from .mongobase import MongoBaseClass


def generate_uuid_str():
    return str(uuid4())

ROLES = {
    'unverified': {
        'description': 'Unverified User'
    },
    'free': {
        'description': 'Free User'
    },
    'paid': {
        'description': 'Paid User',
    },
    'staff': {
        'description': 'Staff User - can have access to cross users',
    },
}

@dataclass
class Role(MongoBaseClass):
    __collectionname__ = 'roles'
    username:str
    role:str
    id:str = field(default_factory=generate_uuid_str)

    def __repr__(self):
        return f'<Role {self.username}={self.role}>'

    def save(self):
        db.db[self.__collectionname__].replace_one({"id": self.id}, self.dict(), upsert=True)

    def delete(self):
        db.db[self.__collectionname__].delete_one({"id": self.id})

    @classmethod
    def get_all_roles_for_user(cls, username):
        roles_list = cls.query.filter_by(username=username).all()
        return [r_db for r_db in roles_list]
    
    @classmethod
    def role_exists_for_user(cls, username, role):

        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return False

        if cls.query.filter_by(username=username, role=role).first() is not None:
            print(f'Role "{role}" exists for user "{username}".')
            return True
        else:
            print(f'Role "{role}" does not exist for user "{username}".')
            return False
    
    @classmethod
    def add_role_for_user(cls, username, role):
        
        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return
        
        if cls.role_exists_for_user(username, role):
            pass
        else:
            new_role = cls(username=username, role=role)
            new_role.save()
            print(f'Role "{role}" added for user "{username}".')

            
    @classmethod
    def remove_role_for_user(cls, username, role):

        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return
        
        if cls.role_exists_for_user(username, role):
            db_role = cls.query.filter_by(username=username, role=role).first()
            db_role.delete()
            print(f'Role "{role}" removed for user "{username}".')
        else:
            print(f'Role "{role}" does not exist for user "{username}".')


'''
from backend.models.user import User, TokenBlocklist 
from backend.models.role import Role

u = User.get_user_by_username(username='salarsatti')
r = Role.get_role_by_username(username='salarsatti')

role = Role(username=user.username, role='free')
'''

