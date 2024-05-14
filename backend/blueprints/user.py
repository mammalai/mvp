from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from backend.models.user import User 

from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

user_bp = Blueprint("users", __name__)

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    claims = get_jwt()
    print(claims)
    claims_roles = claims.get("roles", [])
    if 'staff' in claims_roles:
        page = request.args.get("page", default=1, type=int)

        per_page = request.args.get("per_page", default=3, type=int)

        users = User.query.paginate(page=page, per_page=per_page)

        result = UserSchema().dump(users, many=True)

        return (
            jsonify(
                {
                    "users": result,
                }
            ),
            200,
        )

    return jsonify({"message": "You are not authorized to access this"}), 401