from typing import List, Any, Union, Optional

from pydantic import BaseModel


class Category(BaseModel):
    name: str


class Currency(BaseModel):
    currency: str
    symbol: str
    code: str


class DescriptionClass(BaseModel):
    content: List[Any]
    barcode: None


class Region(BaseModel):
    name: str
    code: str


class ShowingPrice(BaseModel):
    price: int
    showing_currency: Currency


class Catalog(BaseModel):
    sku: int
    upc: int
    title: str
    min_price: float
    max_price: float
    pre_order: bool
    activation_fee: float
    percentage_of_buying_price: int
    currency: Currency
    categories: List[Category]
    regions: List[Region]
    image: str
    description: Union[DescriptionClass, str]
    showing_price: Optional[ShowingPrice]


class CatalogListResponse(BaseModel):
    count: int
    results: List[Catalog]


class CatalogAvailabilityInput(BaseModel):
    product_id: int
    quantity: int
    price: float
