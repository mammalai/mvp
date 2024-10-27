import uuid
import datetime
from dataclasses import dataclass, field
from backend.extensions import db
from .mongobase import MongoBaseClass

@dataclass
class Order(MongoBaseClass):
    __collectionname__ = "orders"
    STATUS_CREATED = "CREATED"
    STATUS_SAVED = "SAVED"
    STATUS_APPROVED = "APPROVED"
    STATUS_VOIDED = "VOIDED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"
    order_id: str
    user_id: str  # Foreign reference to User
    amount: float
    currency: str
    status: str
    description: str
    status: str = field(default=STATUS_CREATED)
    created_at: str
    update_time: str

    def __init__(self, order_details):
        self.order_id = order_details.get("id")
        self.purchase_units = order_details.get("purchase_units")
        self.payment_source = order_details.get("payment_source")
        self.status = order_details.get("status", self.STATUS_CREATED)
        self.created_at = order_details.get("create_time", str(datetime.datetime.now(datetime.timezone.utc)))
        self.update_time = order_details.get("update_time", str(datetime.datetime.now(datetime.timezone.utc)))

    def save(self):
        db.db[self.__collectionname__].replace_one({"id": self.id}, self.dict(), upsert=True)

    def delete(self):
        db.db[self.__collectionname__].delete_one({"id": self.id})
