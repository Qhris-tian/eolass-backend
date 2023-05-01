from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.api_v1.schema import ModelMixin


class Inventory(BaseModel):
    sku: int
    title: str


class CreateInventoryInDB(ModelMixin):
    sku: int
    title: str
    price: Optional[float]


class Card(BaseModel):
    card_number: str
    pin_code: str
    claim_url: str
    expire_date: Optional[datetime | str]
    product: str


class CreateCardInDB(ModelMixin):
    card_number: str
    pin_code: str
    claim_url: str
    expire_date: Optional[datetime | str]
    product: int
