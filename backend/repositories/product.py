# TODO: May need to update to use Motor (Look at other respositories for reference or rather in models...)
from backend.models.mongodb.product import Product

class ProductsRepository():
    def __init__(self, db):
        self.collection = db.products  # TODO: Ensure the collection name matches your MongoDB setup

    async def upsert(self, product: Product) -> None:
        await self.collection.update_one(
            {"id": product.id},
            {"$set": product.__dict__},
            upsert=True
        )

    async def delete(self, product_id: str) -> None:
        await self.collection.delete_one({"id": product_id})

    async def get_by_id(self, product_id: str) -> Product:
        data = await self.collection.find_one({"id": product_id})
        if data:
            return Product(**data)
        return None
    
    async def get_all(self) -> list[Product]:
        products = []
        async for data in self.collection.find():
            products.append(Product(**data))
        return products