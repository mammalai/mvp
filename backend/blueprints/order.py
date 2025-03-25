from fastapi import APIRouter, HTTPException, Request
from backend.payment.services.order_service import OrderService

def create_order_router(order_service: OrderService):
    order_router = APIRouter()

    @order_router.post("/")
    async def create_order(request: Request):
        cart = (await request.json()).get("cart")
        purchase_units = [{"amount": {"currency_code": "USD", "value": "100.00"}}]
        order = order_service.create_order(purchase_units)
        return order.dict()

    @order_router.post("/{order_id}/capture")
    async def capture_order(order_id: str):
        order = order_service.complete_order(order_id)
        return order.dict()

    return order_router
