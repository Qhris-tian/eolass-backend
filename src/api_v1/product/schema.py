from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class Price(BaseModel):
    amount: int
    currency: str


class Auction(BaseModel):
    belongs_to_you: bool
    is_in_stock: bool | None
    merchant_name: str
    price: Price


class Region(BaseModel):
    code: str


class TypeClass(BaseModel):
    value: str


class Product(BaseModel):
    id: UUID
    name: str
    languages: List[str]
    regions: List[Region]
    released_at: datetime
    created_at: datetime
    slug: str
    type: TypeClass
    auctions: List[Auction]


class ProductResponse(BaseModel):
    products: List[Product]
