from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.api_v1.schema import ModelMixin, RWModel


class BaseInventory(BaseModel):
    title: Optional[str]
    price: Optional[float]
    region: Optional[str]


class Inventory(BaseInventory):
    sku: int


class CreateInventoryInDB(Inventory, ModelMixin):
    pass


class UpdateInventoryInDB(BaseInventory, RWModel):
    created_at: datetime | None = Field(
        exclude=True,
    )


class Card(BaseModel):
    card_number: str
    pin_code: str
    claim_url: str
    expire_date: Optional[datetime | str]
    product: str


class CreateCardInDB(ModelMixin):
    card_number: str
    pin_code: Optional[str]
    claim_url: Optional[str]
    expire_date: Optional[datetime | str]
    product: int


class CreateInventoryCardRequest(BaseModel):
    card_number: str
    pin_code: Optional[str]
    claim_url: Optional[str]
    expire_date: Optional[datetime | str]
