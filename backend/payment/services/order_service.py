# order/order_service.py

from backend.models.mongodb.order import Order
from backend.payment.services.payment_service import PaymentService

class OrderService:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
    
    def create_order(self, purchase_units, payment_source):
        """Initiate a payment and create order."""
        order_details = self.payment_service.create_payment(purchase_units, payment_source)

        order = Order(order_details)
        order.save()  # Save the order to the database
        
        return order
    
    def complete_order(self, order_id):
        """Complete the payment and mark the order status."""
        order = Order.get_by_id(order_id)
        
        if not order: # TODO: raise a custom exception
            print("Order not found.")
            return False
        
        order = self.payment_service.execute_payment(order.id)
        order.update(order)
    
    def get_order_status(self, order_id):
        """Return the status of a specific order."""
        order = Order.get_by_id(order_id)
        
        if not order: # TODO: raise a custom exception
            return "Order not found."
        
        return order.status
