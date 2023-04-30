from uuid import UUID
from typing import List, Optional

class Price:
    amount: int = 10
    currency: str = "EUR"

class CreateAuctionMock:
    productId: UUID = "64b399f7-b4b9-1b16-afa5-1526eb11e3a2"
    enabled: bool = 'false'
    keys: Optional[List[str]] = ["key-1-test"]
    autoRenew: bool = 'false'
    price: Price = Price
    onHand: Optional[int]
    declaredStock: Optional[int]