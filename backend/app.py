from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from dotenv import load_dotenv

from backend.blueprints.auth import auth_router
from backend.blueprints.order import create_order_router
from backend.blueprints.products import create_product_router
from backend.blueprints.product_details import create_product_details_router

from backend.services.product import ProductService
from backend.services.product_details import ProductDetailsService

from backend.repositories.product import ProductsRepository
from backend.repositories.product_details import ProductsDetailsRepository

from backend.extensions import db

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
        from backend.services.order import OrderService
        from backend.helpers.paypal_gateway import PayPalGateway

        client_id = os.environ.get("PAYPAL_CLIENT_ID")
        client_secret = os.environ.get("PAYPAL_SECRET")

        # Create instances
        gateway = PayPalGateway(client_id, client_secret)
        order_service = OrderService(gateway)
        
        # Create and include router
        order_router = create_order_router(order_service)
        app.include_router(order_router, prefix="/api/orders")

    # Register auth routes
    app.include_router(auth_router, prefix="/api/auth")

    products_repository = ProductsRepository(db)
    product_service = ProductService(products_repository)
    app.include_router(create_product_router(product_service), prefix="/api/products")

    product_details_repository = ProductsDetailsRepository(db)
    product_details_service = ProductDetailsService(product_details_repository)
    app.include_router(create_product_details_router(product_details_service), prefix="/api/product-details")

    # Echo endpoint
    @app.post("/api/echo")
    async def echo(request: Request):
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="Request must be in JSON format")
        return JSONResponse(content=data)
    
    return app

app = create_app()
