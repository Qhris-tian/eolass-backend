from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.api_v1.schema import ModelMixin


class Product(BaseModel):
    sku: int
    title: str


class Order(BaseModel):
    order_id: int
    delivery_type: Optional[int]
    destination: Optional[str]
    status: int
    status_text: str
    created_time: datetime
    terminal_id: Optional[int]
    product: Product
    count: int
    total_face_value: int
    total_fees: int
    tota_discounts: Optional[float]
    reference_code: Optional[str]
    total_customer_cost: float
    is_completed: bool
    share_link: Optional[str]


class OrderHistory(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Order]


class StatusEnum(Enum):
    pending = "PENDING"
    complete = "COMPLETE"


class CreateOrderRequest(BaseModel):
    product_id: int
    quantity: int
    price: float
    pre_order: bool = Field(default=False)


class CreateOrderInDB(CreateOrderRequest, ModelMixin):
    reference_code: UUID = Field(default_factory=uuid4)
    status: StatusEnum = Field(default=StatusEnum.pending.value)
    auction_id: Optional[str]
