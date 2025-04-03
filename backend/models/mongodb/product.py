import uuid
from dataclasses import dataclass, field

@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price_estimate: int
    category: str
    description: str = ""
    # TODO: Add fields described in Notion

    def update_product(self, new_product: dict):
        for key, value in new_product.items():
            if hasattr(self, key):
                setattr(self, key, value)
