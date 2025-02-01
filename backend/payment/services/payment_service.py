# payment/services/payment_service.py

from backend.payment.gateways.base import PaymentGateway

class PaymentService:
    def __init__(self, gateway: PaymentGateway):
        """Initialize with a specific payment gateway instance."""
        self.gateway = gateway
    
    def create_payment(self, purchase_units, payment_source=None):
        """Create a payment."""
        return self.gateway.initialize_payment(purchase_units, payment_source=payment_source)
    
    def execute_payment(self, order_id):
        """Execute an approved payment."""
        return self.gateway.execute_payment(order_id)
    
    def check_payment_status(self, order_id):
        """Check the current status of a payment."""
        status = self.gateway.get_payment_status(order_id)
        return status
