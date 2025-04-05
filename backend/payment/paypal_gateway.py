import os
from urllib.parse import urljoin
import httpx
from backend.helpers.utils import multi_urljoin
from backend.helpers.errors import PaypalError, MVPError

class PayPalGateway:
    def __init__(self, client_id, client_secret):
        self.base_url = "https://api-m.sandbox.paypal.com" # TODO: Move to paypal config
        self.auth_url = multi_urljoin(self.base_url, "/v1/oauth2/token") # TODO: Move to paypal config
        self.orders_url = multi_urljoin(self.base_url, "/v2/checkout/orders") # TODO: Move to paypal config
        self.client_id = client_id
        self.client_secret = client_secret

    async def __authenticate(self):
        # Define the headers and data payload
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
        }

        # Make the POST request with Basic Authentication
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.auth_url, 
                headers=headers, 
                data=data, 
                auth=(self.client_id, self.client_secret)
            )
            return response.json()

    async def initialize_payment(self, purchase_units, payment_source=None):
        auth_data = await self.__authenticate()
        access_token = auth_data.get("access_token")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        data = {
            "intent": "CAPTURE", # May be changed to "AUTHORIZE" if needed in the future
            "purchase_units": purchase_units
        }

        if payment_source is not None:
            data["payment_source"] = payment_source

        async with httpx.AsyncClient() as client:
            response = await client.post(self.orders_url, headers=headers, json=data)
            order = response.json()
            
            if response.status_code > 399:
                # Handle error response
                raise MVPError("Error creating payment") from PaypalError(
                    name=order.get("name"),
                    message=order.get("message"),
                    status_code=response.status_code,
                    debug_id=order.get("debug_id")
                )

            return order
    
    async def execute_payment(self, order_id):
        auth_data = await self.__authenticate()
        access_token = auth_data.get("access_token")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        url = multi_urljoin(self.orders_url, order_id, 'capture')
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            order = response.json()
            
            if response.status_code > 399:
                # Handle error response
                raise MVPError("Error executing payment") from PaypalError(
                    name=order.get("name"),
                    message=order.get("message"),
                    status_code=response.status_code,
                    debug_id=order.get("debug_id")
                )

            return order
    
    async def get_payment_status(self, order_id):
        auth_data = await self.__authenticate()
        access_token = auth_data.get("access_token")

        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(multi_urljoin(self.orders_url, order_id), headers=headers)
            return response.json().get("status")
