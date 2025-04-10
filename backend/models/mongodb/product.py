import uuid
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price_estimate: int
    category: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # TODO: Add fields described in Notion

    def dict(self):
        return {
            "name": self.name,
            "price_estimate": self.price_estimate,
            "category": self.category,
            "description": self.description,
            "id": self.id
        }

    def update_product(self, new_product: dict):
        for key, value in new_product.items():
            if hasattr(self, key):
                setattr(self, key, value)
