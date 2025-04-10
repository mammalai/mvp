from backend.extensions import db
from backend.models.mongodb.role import Role

class RolesRepository:
    collection = db.roles

    @classmethod
    async def get_by_id(cls, role_id) -> Role | None:
        role = await cls.collection.find_one({"id": role_id}, {"_id": False})
        if role is None:
            return None
        return Role(**role)

    @classmethod
    async def save(cls, role: Role) -> None:
        await cls.collection.update_one(
            {"id": role.id},
            {"$set": role.dict()},
            upsert=True
        )

    @classmethod
    async def delete(self, role_id: str) -> None:
        await self.collection.delete_one({"id": role_id})

    @classmethod
    async def get_all_roles_for_user(cls, username):
        """Get all roles for a user asynchronously"""
        query = await cls.collection.find(
            {"username": username},
            {"_id": False}  # This projection excludes the _id field
        ).to_list(length=None)
        return [Role(**role) for role in query] if query else []
