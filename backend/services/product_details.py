from backend.models.mongodb.product_details import ProductDetails
from backend.repositories.product_details import ProductsDetailsRepository

class ProductDetailsService:
    def __init__(self, repository: ProductsDetailsRepository):
        self.repository = repository

    async def upsert(self, new_product_details: dict) -> ProductDetails:
        product_details = ProductDetails(**new_product_details)
        await self.repository.upsert(product_details)
        return product_details

    async def delete(self, product_details_id: str) -> None:
        await self.repository.delete(product_details_id)

    async def get_product_details_by_id(self, product_details_id: str) -> ProductDetails:
        product_details = await self.repository.get_by_id(product_details_id)
        if not product_details:
            raise ValueError(f"Product details with id {product_details_id} not found")
        return product_details
    
    async def get_all_product_details(self) -> list[ProductDetails]:
        product_details = await self.repository.get_all()
        return product_details