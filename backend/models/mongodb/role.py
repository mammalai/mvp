from dataclasses import dataclass
from backend.helpers.utils import generate_id

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
class Role():
    def __init__(self, username, role: str = 'unverified', id: str = None):
        if not Role.is_role_valid(role):
            raise ValueError(f"Invalid role '{role}'. Valid roles are: {', '.join(ROLES.keys())}")
        self.id = id if id is not None else generate_id()
        self.username = username
        self.role = role

    def __repr__(self):
        return f'<Role {self.username}={self.role}>'
    
    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
    
    @classmethod
    def is_role_valid(cls, role):
        """Check if a role is valid based on the master dictionary"""
        return role in ROLES
