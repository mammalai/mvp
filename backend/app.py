from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from dotenv import load_dotenv

from backend.blueprints.auth import auth_router
from backend.blueprints.order import create_order_router

load_dotenv()

def create_app():
    
    # Initialize FastAPI app
    app = FastAPI()

    # Enable CORS for all routes and origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register order routes if PayPal credentials are available
    if os.environ.get("PAYPAL_CLIENT_ID") and os.environ.get("PAYPAL_SECRET"):
        from backend.payment.services.payment_service import PaymentService
        from backend.payment.services.order_service import OrderService
        from backend.payment.gateways.paypal_gateway import PayPalGateway

        client_id = os.environ.get("PAYPAL_CLIENT_ID")
        client_secret = os.environ.get("PAYPAL_SECRET")

        # Create instances
        gateway = PayPalGateway(client_id, client_secret)
        payment_service = PaymentService(gateway)
        order_service = OrderService(payment_service)
        
        # Create and include router
        order_router = create_order_router(order_service)
        app.include_router(order_router, prefix="/api/orders")

    # Register auth routes
    app.include_router(auth_router, prefix="/api/auth")

    # Echo endpoint
    @app.post("/api/echo")
    async def echo(request: Request):
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="Request must be in JSON format")
        return JSONResponse(content=data)
    
    return app

app = create_app()
