from backend.extensions import db
from backend.models.mongodb.user import User

class UsersRepository:
    collection = db.users

    @classmethod
    async def get_user_by_email(cls, email):
        """return the first user with this email asynchronously"""
        user = await cls.collection.find_one({"email": email}, {"_id": False})
        if user is None:
            return None
        return User.from_dict(user)

    @classmethod
    async def save(cls, user: User) -> None:
        """Save the user to the database asynchronously"""
        # Using upsert here which means update if exists and insert if not
        await cls.collection.update_one(
            {"id": user.id},
            {"$set": user.dict()},
            upsert=True
        )

    @classmethod
    async def delete(cls, id: str) -> None:
        await cls.collection.delete_one({"id": id})
