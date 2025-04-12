from fastapi import APIRouter, Request
from backend.services.product_details import ProductDetailsService

def create_product_details_router(product_details_service: ProductDetailsService):
    product_details_router = APIRouter()

    @product_details_router.post("/")
    async def insert_product_details(request: Request):
        data = await request.json()
        # TODO: Add a layer of validation
        product_details = await product_details_service.upsert(data)
        return product_details.dict() # TODO: Ensure that the returned product is in the correct format

    @product_details_router.post("/{product_details_id}") # TODO: Check if we should use a different HTTP method for upsert
    async def update_product_details(request: Request):
        data = await request.json()
        data["id"] = request.path_params.get("product_details_id")
        # TODO: Add a layer of validation
        product_details = await product_details_service.upsert(data)
        return product_details.dict() # TODO: Ensure that the returned product is in the correct format

    @product_details_router.delete("/{product_details_id}")
    async def delete_product_details(request: Request):
        product_details_id = request.path_params.get("product_details_id")
        if not product_details_id:
            return {"message": "Product ID is required for deletion"}
        await product_details_service.delete(product_details_id)
        return {"message": "Product deleted successfully"} # TODO: Ensure that the response is in the correct format

    return product_details_router
