from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    
    @abstractmethod
    def initialize_payment(self, purchase_units, payment_source=None):
        pass
    
    @abstractmethod
    def execute_payment(self, order_id):
        pass
    
    @abstractmethod
    def get_payment_status(self, order_id):
        pass
