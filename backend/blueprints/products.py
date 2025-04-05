from fastapi import APIRouter, Request
from backend.services.product import ProductService

def create_product_router(product_service: ProductService):
    product_router = APIRouter()

    @product_router.post("/")
    async def insert_product(request: Request):
        data = await request.json()
        # TODO: Add a layer of validation
        product = await product_service.upsert(data)
        return product.dict() # TODO: Ensure that the returned product is in the correct format

    @product_router.post("/{product_id}") # TODO: Check if we should use a different HTTP method for upsert
    async def update_product(request: Request):
        data = await request.json()
        data["id"] = request.path_params.get("product_id")
        # TODO: Add a layer of validation
        product = await product_service.upsert(data)
        return product.dict() # TODO: Ensure that the returned product is in the correct format

    @product_router.delete("/{product_id}")
    async def delete_product(request: Request):
        product_id = request.path_params.get("product_id")
        if not product_id:
            return {"message": "Product ID is required for deletion"}
        await product_service.delete(product_id)
        return {"message": "Product deleted successfully"} # TODO: Ensure that the response is in the correct format

    return product_router
