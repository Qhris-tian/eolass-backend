from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel


class Price(BaseModel):
    amount: int
    currency: str

class CreateAuctionRequest(BaseModel):
    type: str
    productId: UUID
    enabled: bool
    keys: Optional[List[str]]
    autoRenew: bool
    price: Price
    onHand: Optional[int] = 0
    declaredStock: Optional[int] = 0

