from uuid import UUID
from typing import List, Optional, Union

from pydantic import BaseModel


class Price(BaseModel):
    amount: int
    currency: str

class CreateAuctionRequest(BaseModel):
    productId: UUID
    enabled: Union[bool, str]
    keys: Optional[List[str]]
    autoRenew: Union[bool, str]
    price: Price
    onHand: Optional[int]
    declaredStock: Optional[int]

class UpdateAuctionRequest(BaseModel):
    id: UUID
    price: Optional[Price]
    addedKeys: Optional[List[str]]
    acquisitionPrice: Optional[Price]
    removedKeys: Optional[List[str]]
    enabled: Union[bool, str] = False
    autoRenew: Union[bool, str] = False
    lowStockNotificationEnabled: bool = False
    priceChangeNotificationEnabled: bool = False
    declaredStock: Optional[int]
