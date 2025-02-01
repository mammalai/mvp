import os
from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth
from backend.payment.gateways.base import PaymentGateway
from backend.helpers.utils import multi_urljoin
from backend.helpers.errors import PaypalError, MVPError

class PayPalGateway(PaymentGateway):
    def __init__(self, client_id, client_secret):
        self.base_url = "https://api-m.sandbox.paypal.com" # TODO: Move to paypal config
        self.auth_url = multi_urljoin(self.base_url, "/v1/oauth2/token") # TODO: Move to paypal config
        self.orders_url = multi_urljoin(self.base_url, "/v2/checkout/orders") # TODO: Move to paypal config
        self.client_id = client_id
        self.client_secret = client_secret

    def __authenticate(self):
        # Define the headers and data payload
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
        }

        # Make the POST request with Basic Authentication
        response = requests.post(self.auth_url, headers=headers, data=data, auth=HTTPBasicAuth(self.client_id, self.client_secret))

        # Response contains the following:
        # {
        #     "scope": "https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller https://uri.paypal.com/services/payments/refund https://api-m.paypal.com/v1/vault/credit-card https://api-m.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://api-m.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks",
        #     "access_token": "A21AAFEpH4PsADK7qSS7pSRsgzfENtu-Q1ysgEDVDESseMHBYXVJYE8ovjj68elIDy8nF26AwPhfXTIeWAZHSLIsQkSYz9ifg",
        #     "token_type": "Bearer",
        #     "app_id": "APP-80W284485P519543T",
        #     "expires_in": 31668,
        #     "nonce": "2020-04-03T15:35:36ZaYZlGvEkV4yVSz8g6bAKFoGSEzuy3CQcz3ljhibkOHg"
        # }
        return response.json()

    def initialize_payment(self, purchase_units, payment_source=None):
        access_token = self.__authenticate().get("access_token")
        headers = {
            'Content-Type': 'application/json',
            # 'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
            'Authorization': f'Bearer {access_token}', # TODO: Try using f'Basic self.client_id:self.secret' instead
        }

        data = {
            "intent": "CAPTURE", # May be changed to "AUTHORIZE" if needed in the future
            "purchase_units": purchase_units
        }

        # data = '{ "intent": "CAPTURE", "purchase_units": [ { "amount": { "currency_code": "USD", "value": "100.00" } } ] }'
        # data = json.dumps(data)

        if payment_source is not None:
            data["payment_source"] = payment_source

        response = requests.post(self.orders_url, headers=headers, json=data)
        # Response contains the following (there are more fields):
        # {
        #     "id": "5O190127TN364720T", <--- This is the order ID
        #     "status": "CREATED", <--- This is the order status
        #     ...
        # }
        order = response.json()
        if response.status_code > 399:
            # Handle error response
            raise MVPError("Error creating payment") from PaypalError(
                name=order.get("name"),
                message=order.get("message"),
                status_code=response.status_code,
                debug_id=order.get("debug_id")
            )
        
        # {
        #     'id': '1PN63320AH9169723',
        #     'status': 'CREATED',
        #     'links': [
        #         {
        #             'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/1PN63320AH9169723',
        #             'rel': 'self',
        #             'method': 'GET'
        #         },
        #         {
        #             'href': 'https://www.sandbox.paypal.com/checkoutnow?token=1PN63320AH9169723',
        #             'rel': 'approve',
        #             'method': 'GET'
        #         },
        #         {
        #             'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/1PN63320AH9169723',
        #             'rel': 'update',
        #             'method': 'PATCH'
        #         },
        #         {
        #             'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/1PN63320AH9169723/capture',
        #             'rel': 'capture',
        #             'method': 'POST'
        #         }
        #     ]
        # }

        return order
    
    def execute_payment(self, order_id):
        access_token = self.__authenticate().get("access_token")

        headers = {
            'Content-Type': 'application/json',
            # 'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
            'Authorization': f'Bearer {access_token}', # TODO: Try using f'Basic self.client_id:self.secret' instead
        }

        url = multi_urljoin(self.orders_url, order_id, 'capture')
        response = requests.post(url, headers=headers)

        order = response.json()
        if response.status_code > 399:
            # Handle error response
            raise MVPError("Error executing payment") from PaypalError(
                name=order.get("name"),
                message=order.get("message"),
                status_code=response.status_code,
                debug_id=order.get("debug_id")
            )

        # response = requests.get(multi_urljoin(self.orders_url, order_id), headers=headers)

        # print("Order after executing payment:", order)
        return order
    
    def get_payment_status(self, order_id):
        access_token = self.__authenticate().get("access_token")

        headers = {
            'Authorization': f'Bearer {access_token}', # TODO: Try using f'Basic self.client_id:self.secret' instead
        }
        response = requests.get(multi_urljoin(self.orders_url, order_id), headers=headers)
        return response.json().get("status")
