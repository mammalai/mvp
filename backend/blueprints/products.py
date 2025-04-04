from fastapi import APIRouter, Request
from backend.services.product import ProductService


from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal


class ProductTableItem(BaseModel):
    category: str
    why_this_one: List[str]
    price: str
    link: str  # Consider using HttpUrl if you want URL validation


class WhatToLookFor(BaseModel):
    description: str
    no_brainers: List[str]
    things_to_think_about: List[str]


class ProductDetails(BaseModel):
    """
    This is the format of the data that is expected to be sent to the API.
    """
    title: str
    category: str
    price_estimate: str
    usefulness_knee_hip_surgery: Literal["low", "medium", "high"]
    usefulness_stroke_and_brain_injury: Literal["low", "medium", "high"]
    usefulness_aging_in_place: Literal["low", "medium", "high"]
    
    initial_description: str
    product_table: List[ProductTableItem]
    what_to_look_for: WhatToLookFor
    more_to_consider: str



def create_product_router(product_service: ProductService):
    product_router = APIRouter()

    @product_router.post("/")
    async def insert_product(request: Request):
        data = await request.json()
        # TODO: Add a layer of validation
        # TODO: Add a layer that converts the incoming data to the expected format
        product = await product_service.upsert(data)
        return product.dict() # TODO: Ensure that the returned product is in the correct format

    @product_router.post("/{product_id}") # TODO: Check if we should use a different HTTP method for upsert
    async def update_product(request: Request):
        data = await request.json()
        data["id"] = request.path_params.get("product_id")
        # TODO: Add a layer of validation
        # TODO: Add a layer that converts the incoming data to the expected format
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
