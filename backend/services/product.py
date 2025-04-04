from backend.models.mongodb.product import Product
from backend.repositories.product import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def upsert(self, new_product: dict) -> Product:
        product = Product(**new_product)
        await self.repository.upsert(product)
        return product

    async def delete_product(self, product_id: str) -> None:
        await self.repository.delete(product_id)

    async def get_product_by_id(self, product_id: str) -> Product:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product
    
    async def get_all_products(self) -> list[Product]:
        products = await self.repository.get_all()
        return products