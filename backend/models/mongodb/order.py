import uuid
import datetime
from dataclasses import dataclass, field
from backend.extensions import db
from .mongobase import MongoBaseClass

# @dataclass
class Order(MongoBaseClass):
    """
    This is a class that manages the orders and the data and the interaction with the database (currently only supports paypa;)
    """
    __collectionname__ = "orders"
    STATUS_CREATED = "CREATED"
    STATUS_SAVED = "SAVED"
    STATUS_APPROVED = "APPROVED"
    STATUS_VOIDED = "VOIDED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"
    id: str
    user_id: str  # Foreign reference to User
    amount: float
    currency: str
    status: str
    description: str
    status: str = field(default=STATUS_CREATED)
    create_time: str
    update_time: str

    def __init__(self, order_details):
        """
        order_details is a json that is created by paypal and is primarily used to create the order object
        """
        self.id = order_details.get("id")
        self.status = order_details.get("status", 'UNKNOWN')
        self.payment_source = order_details.get("payment_source")
        self.purchase_units = order_details.get("purchase_units")
        self.payer = order_details.get("payer")
        self.links = order_details.get("links")
        self.create_time = order_details.get("create_time", str(datetime.datetime.now(datetime.timezone.utc)))
        self.update_time = order_details.get("update_time", str(datetime.datetime.now(datetime.timezone.utc)))

    @classmethod
    def get_by_id(cls, order_id):
        order = db.db[cls.__collectionname__].find_one({"id": order_id}, {"_id": False})
        if order is None:
            return None
        return cls(order)

    def __repr__(self):
        return f"Order: {self.id}, {self.status}"
    
    def dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "payment_source": self.payment_source,
            "purchase_units": self.purchase_units,
            "payer": self.payer,
            "links": self.links,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
    
    def update(self, order_details):
        print('Updating order:', order_details)
        self.id = order_details.get("id")
        self.status = order_details.get("status", 'UNKNOWN')
        self.payment_source = order_details.get("payment_source")
        self.purchase_units = order_details.get("purchase_units")
        self.payer = order_details.get("payer")
        self.links = order_details.get("links")
        self.create_time = order_details.get("create_time", str(datetime.datetime.now(datetime.timezone.utc)))
        self.update_time = order_details.get("update_time", str(datetime.datetime.now(datetime.timezone.utc)))
        self.save()

    def save(self):
        db.db[self.__collectionname__].replace_one({"id": self.id}, self.dict(), upsert=True)

    def delete(self):
        db.db[self.__collectionname__].delete_one({"id": self.id})
