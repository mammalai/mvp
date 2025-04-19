from fastapi import APIRouter, Request, Depends, HTTPException, status
from backend.services.product_details import ProductDetailsService
from backend.models.mongodb.user import User
from backend.models.mongodb.role import Role, RoleName
from backend.middleware.auth import decode_access_token

def admin_required(user: User = Depends(decode_access_token)):
    if not user.has_role(Role(RoleName.ADMIN)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user

def create_product_details_router(product_details_service: ProductDetailsService):
    product_details_router = APIRouter()

    @product_details_router.post("/", dependencies=[Depends(admin_required)])
    async def insert_product_details(request: Request):
        data = await request.json()
        product_details = await product_details_service.upsert(data)
        return product_details.dict()

    @product_details_router.post("/{product_details_id}", dependencies=[Depends(admin_required)])
    async def update_product_details(request: Request):
        data = await request.json()
        data["id"] = request.path_params.get("product_details_id")
        product_details = await product_details_service.upsert(data)
        return product_details.dict()

    @product_details_router.delete("/{product_details_id}", dependencies=[Depends(admin_required)])
    async def delete_product_details(request: Request):
        product_details_id = request.path_params.get("product_details_id")
        if not product_details_id:
            return {"message": "Product ID is required for deletion"}
        await product_details_service.delete(product_details_id)
        return {"message": "Product deleted successfully"}

    return product_details_router
