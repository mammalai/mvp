import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
from backend.app import create_app, db
from backend.models import User
from backend.config import TestConfig
from backend.payment.gateways.paypal_gateway import PayPalGateway

@pytest.fixture
def client():
	app = create_app()
	
	if os.environ.get("DB_TYPE") == "mongodb":
		with app.test_client() as testclient:
			with app.app_context():
				# clean up the database before running the test
				db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
				yield testclient
		# drop the database after running the test
		db.cx.drop_database(f'{TestConfig.PROJECT_NAME}')
	elif os.environ.get("DB_TYPE") == "sqlalchemy":
		with app.test_client() as testclient:
			with app.app_context():
				db.create_all()
				yield testclient
	else:
		raise Exception("DB_TYPE not set in configuration.")

@pytest.fixture
def strong_password():
    return "StrongPassword123"

def test_payment(client, strong_password):
	with client.application.app_context():
		client_id = client.application.config.get("PAYPAL_CLIENT_ID")
		secret = client.application.config.get("PAYPAL_SECRET")

		gateway = PayPalGateway(client_id, secret)
		purchase_units = [
			{
				# "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b", # TODO: This should come from the request
				"amount": {
					"currency_code": "USD",
					"value": "100.00"
				}
			}
		]
		payment_source = { # TODO: This should come from the request
			"paypal": {
				"experience_context": {
					"payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
					"locale": "en-US",
					"landing_page": "LOGIN",
					"user_action": "PAY_NOW",
				}
			}
		}
		order = gateway.initialize_payment(purchase_units, payment_source=payment_source)
		assert order.get("status") == "PAYER_ACTION_REQUIRED"
		assert order.get("id") is not None

		# Simulate capturing the payment
		# capture_response = gateway.execute_payment(order.get("id"))
		# assert capture_response.get("status") == "COMPLETED"
		# assert capture_response.get("id") == order.get("id")
