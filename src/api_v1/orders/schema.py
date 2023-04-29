from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    sku: int
    title: str


class Order(BaseModel):
    order_id: int
    delivery_type: int
    destination: str
    status: int
    status_text: str
    created_time: datetime
    terminal_id: int
    product: Product
    count: int
    total_face_value: int
    total_fees: int
    tota_discounts: float
    total_customer_cost: float
    is_completed: bool
    share_link: str


class OrderHistory(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    result: List[Order]


class CreateOrderRequest(BaseModel):
    product_id: int
    quantity: int
    price: float
