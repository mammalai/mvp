from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from backend.helpers.utils import generate_id

class ProductTableItem(BaseModel):
    category: str
    why_this_one: List[str]
    price: str
    link: str  # Consider using HttpUrl if you want URL validation


class WhatToLookFor(BaseModel):
    description: str
    no_brainers: List[str]
    things_to_think_about: List[str]


class ProductDetails(BaseModel):
    """
    This is the format of the data that is expected to be sent to the API.
    """
    id: str = Field(default_factory=generate_id)
    title: str
    category: str
    price_estimate: str
    usefulness_knee_hip_surgery: Literal["low", "medium", "high"]
    usefulness_stroke_and_brain_injury: Literal["low", "medium", "high"]
    usefulness_aging_in_place: Literal["low", "medium", "high"]

    initial_description: str
    product_table: List[ProductTableItem]
    what_to_look_for: WhatToLookFor
    more_to_consider: str