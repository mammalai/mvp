from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    
    @abstractmethod
    def initialize_payment(self, amount, currency, description):
        pass
    
    @abstractmethod
    def execute_payment(self, payment_id, payer_id):
        pass
    
    @abstractmethod
    def get_payment_status(self, payment_id):
        pass
