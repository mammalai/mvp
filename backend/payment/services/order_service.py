# order/order_service.py

from backend.models.mongodb.order import Order
from backend.payment.services.payment_service import PaymentService

class OrderService:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
    
    async def create_order(self, purchase_units, payment_source=None):
        """Initiate a payment and create order."""
        order_details = await self.payment_service.create_payment(purchase_units, payment_source=payment_source)

        order = Order(order_details)
        await order.save()  # Save the order to the database
        
        return order
    
    async def complete_order(self, order_id):
        """Complete the payment and mark the order status."""
        order = await Order.get_by_id(order_id)
        
        if not order: # TODO: raise a custom exception
            print("Order not found.")
            return False
        
        order_details = await self.payment_service.execute_payment(order.id)
        # Save order to the database
        await order.update(order_details)
        return order
    
    async def get_order_status(self, order_id):
        """Return the status of a specific order."""
        order = await Order.get_by_id(order_id)
        
        if not order: # TODO: raise a custom exception
            return "Order not found."
        
        return order.status
