from dataclasses import dataclass
from enum import Enum

class RoleName(Enum):
    ADMIN = "admin"
    UNVERIFIED = "unverified"
    FREE = "free"
    PAID = "paid"
    STAFF = "staff"

@dataclass
class Role():
    def __init__(self, name: RoleName = RoleName.UNVERIFIED):
        if not Role.is_valid(name):
            raise ValueError(f"Invalid role '{name}'. Valid roles are: {', '.join([r.value for r in RoleName])}")
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'
    
    def __eq__(self, other):
        return isinstance(other, Role) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name.value
    
    @classmethod
    def is_valid(cls, role: RoleName):
        return isinstance(role, RoleName)
