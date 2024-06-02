from flask import Flask, jsonify, request

import sys
from backend.blueprints.auth import auth_bp
from backend.blueprints.user import user_bp
from backend.models.user import User
from backend.models.token import TokenBlocklist
from backend.extensions import db, jwt
from datetime import timedelta

import os
from backend.config import TestConfig, DevConfig, ProdConfig


def create_app():
    app = Flask(__name__)

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

    # register bluepints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.route('/echo', methods=['POST'])
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
        identity = jwt_data["sub"]

        return User.query.filter_by(username=identity).one_or_none()

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
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):        
        jti = jwt_data['jti']

        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None

    return app