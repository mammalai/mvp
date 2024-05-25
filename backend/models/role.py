from backend.extensions import db
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return uuid4()


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

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(), primary_key=True, default=str(generate_uuid()))
    username = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f'<Role {self.username}={self.role}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
            pass


'''
from backend.models.user import User, TokenBlocklist 
from backend.models.role import Role

u = User.get_user_by_username(username='salarsatti')
r = Role.get_role_by_username(username='salarsatti')

role = Role(username=user.username, email=user.email, role='free')
'''

