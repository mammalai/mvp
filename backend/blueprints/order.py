from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

def create_order_blueprint(order_service):
    order_bp = Blueprint("orders", __name__)

    @order_bp.post("")
    def create_order():
        print("CREATING ORDER V2...")
        # TODO: compute purchase_units from cart
        cart = request.get_json().get("cart")

        purchase_units = [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }
        ]

        print('purchase_units:', purchase_units)
        order = order_service.create_order(purchase_units)
        print('order:', order.dict(), repr(order))

        return jsonify(order.dict()), 200

    @order_bp.post("/<order_id>/capture")
    def capture_order(order_id):
        order = order_service.complete_order(order_id)
        return jsonify(order.dict()), 200

    return order_bp
