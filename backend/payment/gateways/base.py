from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    
    @abstractmethod
    async def initialize_payment(self, purchase_units, payment_source=None):
        pass
    
    @abstractmethod
    async def execute_payment(self, order_id):
        pass
    
    @abstractmethod
    async def get_payment_status(self, order_id):
        pass
