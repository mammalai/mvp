import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.payment.paypal_gateway import PayPalGateway
import os

@pytest.mark.asyncio
async def test_payment(client):
    """
    Test PayPal payment initialization and processing
    """
    # Get credentials from environment variables instead of app context
    client_id = os.environ.get("PAYPAL_CLIENT_ID")
    secret = os.environ.get("PAYPAL_SECRET")

    # Create the gateway
    gateway = PayPalGateway(client_id, secret)
    
    # Setup payment data
    purchase_units = [
        {
            "amount": {
                "currency_code": "USD",
                "value": "100.00"
            }
        }
    ]
    
    payment_source = {
        "paypal": {
            "experience_context": {
                "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                "locale": "en-US",
                "landing_page": "LOGIN",
                "user_action": "PAY_NOW",
            }
        }
    }
    
    # Initialize payment - check if PayPalGateway.initialize_payment is async
    # If it's async, use: order = await gateway.initialize_payment(...)
    # If it's synchronous, use:
    order = await gateway.initialize_payment(purchase_units, payment_source=payment_source)
    
    # Assertions
    assert order.get("status") == "PAYER_ACTION_REQUIRED"
    assert order.get("id") is not None

    # Commented out section - also update if needed
    # If gateway.execute_payment is async, use: await gateway.execute_payment(...)
    # capture_response = gateway.execute_payment(order.get("id"))
    # assert capture_response.get("status") == "COMPLETED"
    # assert capture_response.get("id") == order.get("id")
