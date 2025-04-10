from fastapi import APIRouter, HTTPException, Request
from backend.services.order import OrderService

def create_order_router(order_service: OrderService):
    order_router = APIRouter()

    @order_router.post("/")
    async def create_order(request: Request):
        data = await request.json()
        cart = data.get("cart")
        purchase_units = [{"amount": {"currency_code": "USD", "value": "100.00"}}]
        order = await order_service.create_order(purchase_units)
        return order.dict()

    @order_router.post("/{order_id}/capture")
    async def capture_order(order_id: str):
        order = await order_service.complete_order(order_id)
        return order.dict()

    @order_router.get("/{order_id}")
    async def get_order(order_id: str):
        status = await order_service.get_order_status(order_id)
        return {"order_id": order_id, "status": status}

    return order_router
