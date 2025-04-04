import uuid
import datetime
from dataclasses import dataclass, field
from backend.extensions import db
from .mongobase import MongoBaseClass

@dataclass
class Order(MongoBaseClass):
    """
    This is a class that manages the orders and the data and the interaction with the database (currently only supports paypal)
    """
    __collectionname__ = "orders"
    STATUS_CREATED = "CREATED"
    STATUS_SAVED = "SAVED"
    STATUS_APPROVED = "APPROVED"
    STATUS_VOIDED = "VOIDED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"
    id: str = None
    status: str = field(default=STATUS_CREATED)
    payment_source: dict = None
    purchase_units: list = None
    payer: dict = None
    links: list = None
    create_time: str = None
    update_time: str = None

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
    async def get_by_id(cls, order_id):
        order = await db[cls.__collectionname__].find_one({"id": order_id}, {"_id": False})
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
    
    async def update(self, order_details):
        print('Updating order:', order_details)
        self.id = order_details.get("id")
        self.status = order_details.get("status", 'UNKNOWN')
        self.payment_source = order_details.get("payment_source")
        self.purchase_units = order_details.get("purchase_units")
        self.payer = order_details.get("payer")
        self.links = order_details.get("links")
        self.create_time = order_details.get("create_time", str(datetime.datetime.now(datetime.timezone.utc)))
        self.update_time = order_details.get("update_time", str(datetime.datetime.now(datetime.timezone.utc)))
        await self.save()

    async def save(self):
        await db[self.__collectionname__].replace_one({"id": self.id}, self.dict(), upsert=True)

    async def delete(self):
        await db[self.__collectionname__].delete_one({"id": self.id})
