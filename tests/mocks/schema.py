from typing import List, Optional
from uuid import UUID


class Price:
    amount: int = 10
    currency: str = "EUR"


class CreateAuctionMock:
    productId: UUID = "64b399f7-b4b9-1b16-afa5-1526eb11e3a2"
    enabled: bool = "false"
    keys: Optional[List[str]] = ["key-1-test"]
    autoRenew: bool = "false"
    price: Price = Price
    onHand: Optional[int] = 0
    declaredStock: Optional[int] = 0


class UpdateAuctionMock:
    id: UUID = "64b399f7-b4b9-1b16-afa5-1526eb11e3a2"
    price: Optional[Price] = Price
    addedKeys: Optional[List[str]] = []
    acquisitionPrice: Optional[Price]
    removedKeys: Optional[List[str]] = []
    enabled: Optional[bool] = False
    autoRenew: Optional[bool] = False
    lowStockNotificationEnabled: Optional[bool] = False
    priceChangeNotificationEnabled: Optional[bool] = False
    declaredStock: Optional[int] = 0
