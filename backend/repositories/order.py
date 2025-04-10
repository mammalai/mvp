from backend.extensions import db
from backend.models.mongodb.order import Order

class OrdersRepository:
    collection = db.orders

    @classmethod
    async def get_by_id(cls, order_id) -> Order | None:
        order = await cls.collection.find_one({"id": order_id}, {"_id": False})
        if order is None:
            return None
        return Order(**order)

    @classmethod
    async def save(cls, order: Order) -> None:
        await cls.collection.update_one(
            {"id": order.id},
            {"$set": order.dict()},
            upsert=True
        )

    @classmethod
    async def delete(self, order_id: str) -> None:
        await self.collection.delete_one({"id": order_id})
