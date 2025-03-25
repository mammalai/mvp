from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import timedelta
import os

from backend.blueprints.auth import auth_router
from backend.blueprints.order import create_order_router
from backend.extensions import db, jwt
from backend.config import TestConfig, DevConfig, ProdConfig

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

# Load configuration based on environment
if os.environ.get("FLASK_ENV") == "TEST" or os.environ.get("FLASK_ENV") is None:
    config = TestConfig
elif os.environ.get("FLASK_ENV") == "DEV":
    config = DevConfig
elif os.environ.get("FLASK_ENV") == "PROD":
    config = ProdConfig
else:
    raise Exception("At least one config has not been set")

# Initialize extensions
db.init_app(app)
jwt.init_app(app)

# Register order routes if PayPal credentials are available
if config.PAYPAL_CLIENT_ID and config.PAYPAL_SECRET:
    from backend.payment.services.payment_service import PaymentService
    from backend.payment.services.order_service import OrderService
    from backend.payment.gateways.paypal_gateway import PayPalGateway

    client_id = config.PAYPAL_CLIENT_ID
    client_secret = config.PAYPAL_SECRET

    order_service = OrderService(PaymentService(PayPalGateway(client_id, client_secret)))
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

# JWT user lookup callback
@jwt.user_lookup_loader
def user_lookup_callback(jwt_data):
    identity = jwt_data["sub"]
    return identity

# Additional claims loader
@jwt.additional_claims_loader
def make_additional_claims(identity):
    return {"is_staff": identity == "janedoe123"}

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return JSONResponse(
        content={"message": "Token has expired", "error": "token_expired"}, status_code=401
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return JSONResponse(
        content={"message": "Signature verification failed", "error": "invalid_token"},
        status_code=401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return JSONResponse(
        content={"message": "Request doesn't contain a valid token", "error": "authorization_header"},
        status_code=401,
    )