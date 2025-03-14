from flask import Flask, jsonify, request
from flask_cors import CORS

import sys
from backend.blueprints.auth import auth_bp

from backend.extensions import db, jwt

from datetime import timedelta

import os
from backend.config import TestConfig, DevConfig, ProdConfig


def create_app():
    app = Flask(__name__)

    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Enable CORS for all routes and origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # if no environment variable, it will default to test
    if os.environ.get("FLASK_ENV") == "TEST" or os.environ.get("FLASK_ENV") == None:
        app.config.from_object(TestConfig)
    elif os.environ.get("FLASK_ENV") == "DEV":
        app.config.from_object(DevConfig)
    elif os.environ.get("FLASK_ENV") == "PROD":
        app.config.from_object(ProdConfig)
    else:
        raise Exception("At least one config has not been set")
   
    # initialize exts
    db.init_app(app)
    jwt.init_app(app)

    if app.config.get("PAYPAL_CLIENT_ID") and app.config.get("PAYPAL_SECRET"):
        from backend.blueprints.order import create_order_blueprint
        from backend.payment.services.payment_service import PaymentService
        from backend.payment.services.order_service import OrderService
        from backend.payment.gateways.paypal_gateway import PayPalGateway
        # I got them from here: https://developer.paypal.com/dashboard/accounts/edit/5325186290147400380?accountName=sb-phbab33627723@business.example.com
        client_id = app.config.get("PAYPAL_CLIENT_ID")
        client_secret = app.config.get("PAYPAL_SECRET")

        order_service = OrderService(PaymentService(PayPalGateway(client_id, client_secret)))

        order_bp = create_order_blueprint(order_service)

        app.register_blueprint(order_bp, url_prefix="/api/orders")


    # register bluepints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(user_bp, url_prefix="/api/users")

    @app.route('/api/echo', methods=['POST'])
    def echo():
        # Check if the request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400

        # Retrieve JSON data from the request
        data = request.json

        # Echo back the received JSON data
        return jsonify(data)

    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        """
        This function will be called whenever a protected route is accessed e.g. protected by @jwt_required()
        And it is a callback to get data bout the user
        """
        identity = jwt_data["sub"]
        return identity
    # this will go to the database and get everything about the user
    #     return User.query.filter_by(email=identity).one_or_none()

    # additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "janedoe123":
            return {"is_staff": True}
        return {"is_staff": False}

    # jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request doesnt contain valid token",
                    "error": "authorization_header",
                }
            ),
            401,
        )
    

    """
    This function is called whenever a valid JWT is used to access a protected route. The callback will receive the JWT header and JWT payload as arguments, and must return True if the JWT has been revoked.

    Once you scale out the recommended way to use a tokenblock list is to use a redis cache.

    More info:https://stackoverflow.com/questions/21978658/invalidating-json-web-tokens

    """
    # @jwt.token_in_blocklist_loader
    # def token_in_blocklist_callback(jwt_header, jwt_data):        
    #     jti = jwt_data['jti']

    #     token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

    #     return token is not None

    return app