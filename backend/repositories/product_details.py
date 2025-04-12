from backend.models.mongodb.product_details import ProductDetails

class ProductsDetailsRepository():
    def __init__(self, db):
        self.collection = db.product_details

    async def upsert(self, product_details: ProductDetails) -> None:
        await self.collection.update_one(
            {"id": product_details.id},
            {"$set": product_details.dict()},
            upsert=True
        )

    async def delete(self, product_details_id: str) -> None:
        await self.collection.delete_one({"id": product_details_id})

    async def get_by_id(self, product_details_id: str) -> ProductDetails:
        data = await self.collection.find_one({"id": product_details_id})
        if data:
            return ProductDetails(**data)
        return None
    
    async def get_all(self) -> list[ProductDetails]:
        product_details = []
        async for data in self.collection.find():
            product_details.append(ProductDetails(**data))
        return product_details