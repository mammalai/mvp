from backend.models.mongodb.role import Role
from backend.repositories.role import RolesRepository

class RoleService:    
    @classmethod
    async def role_exists_for_user(cls, username, role):
        """Check if a role exists for a user asynchronously"""
        if Role.is_role_valid(role) is False:
            return False

        roles = await RolesRepository.get_all_roles_for_user(username)
        
        for r in roles:
            if r.role == role:
                return True
            
        return False
    
    @classmethod
    async def add_role_for_user(cls, username, role):
        """Add a role for a user asynchronously"""
        if Role.is_role_valid(role) is False:
            return False
        
        saved_roles = await RolesRepository.get_all_roles_for_user(username)

        for saved_role in saved_roles:
            if saved_role.role == role:
                return saved_role
            
        new_role = Role(username=username, role=role)
        await RolesRepository.save(new_role)
        return new_role
    
    @classmethod
    async def remove_role_for_user(cls, username, role):
        """Remove a role from a user asynchronously"""
        if Role.is_role_valid(role) is False:
            return False
        
        roles = await RolesRepository.get_all_roles_for_user(username)
        
        for r in roles:
            if r.role == role:
                await RolesRepository.delete(r.id)
