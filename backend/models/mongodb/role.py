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

    async def save(self):
        """Save the role to the database asynchronously"""
        await db[self.__collectionname__].replace_one(
            {"id": self.id}, 
            self.dict(), 
            upsert=True
        )

    async def delete(self):
        """Delete the role from the database asynchronously"""
        await db[self.__collectionname__].delete_one({"id": self.id})

    @classmethod
    async def get_all_roles_for_user(cls, username):
        """Get all roles for a user asynchronously"""
        query = await cls.query.filter_by(username=username)
        return await query.all()
    
    @classmethod
    async def role_exists_for_user(cls, username, role):
        """Check if a role exists for a user asynchronously"""
        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return False

        query = await cls.query.filter_by(username=username, role=role)
        role_obj = await query.first()
        
        if role_obj is not None:
            print(f'Role "{role}" exists for user "{username}".')
            return True
        else:
            print(f'Role "{role}" does not exist for user "{username}".')
            return False
    
    @classmethod
    async def add_role_for_user(cls, username, role):
        """Add a role for a user asynchronously"""
        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return
        
        if await cls.role_exists_for_user(username, role):
            pass
        else:
            new_role = cls(username=username, role=role)
            await new_role.save()
            print(f'Role "{role}" added for user "{username}".')

            
    @classmethod
    async def remove_role_for_user(cls, username, role):
        """Remove a role from a user asynchronously"""
        if role not in ROLES:
            print(f'Role "{role}" does not exist in master dictionary. Please check the role or update the master dictionary.')
            return
        
        if await cls.role_exists_for_user(username, role):
            query = await cls.query.filter_by(username=username, role=role)
            db_role = await query.first()
            await db_role.delete()
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

