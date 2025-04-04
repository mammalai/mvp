
from .mongobase import MongoBaseClass
import uuid
from dataclasses import dataclass, field
from enum import Enum


class CharacteristicTypeEnum(Enum):
    NO_BRAINER = "noBrainer"
    THINGS_TO_THINK_ABOUT = "thingsToThinkAbout"
    WHAT_TO_LOOK_FOR = "whatToLookFor"
    MORE_TO_CONSIDER = "moreToConsider"

@dataclass
class Characteristic:
    type: CharacteristicTypeEnum 
    name: str
    value: str


@dataclass
class ProductOption:
    rating: str
    image_url: str
    why_this_one: list[str]
    price: str
    link: str

class CategoryEnum(Enum):
    BATHROOM_SAFETY = "bathroomSafety"
    MOBILITY_ASSISTANCE = "mobilityAssistance"
    BEDROOM_COMFORT = "bedroomComfort"
    KITCHEN_INDEPENDENCE = "kitchenIndependence"
    DRESSING_TOOLS = "dressingTools"
    SECURITY_AND_EMERGENCY = "securityAndEmergency"

@dataclass
class Product(MongoBaseClass):
    # TODO: make enums and nested dataclasses for objects are supported in the mongobasclass

    __collectionname__ = "products"

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price_estimate: float
    category: CategoryEnum
    usefulness_for: str
    title: str
    description: str = ""
    
    characteristics: list[Characteristic] = field(default_factory=list)
    
    productOptions: list[ProductOption] = field(default_factory=list)

    def update_product(self, new_product: dict):
        for key, value in new_product.items():
            if hasattr(self, key):
                setattr(self, key, value)
