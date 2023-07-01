from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from src.api_v1.schema import ModelMixin


class Price(BaseModel):
    amount: int
    currency: str


class CreateAuctionRequest(BaseModel):
    productId: UUID
    enabled: Union[bool, str]
    keys: List[str]
    autoRenew: Union[bool, str]
    price: Price
    onHand: Optional[int]
    declaredStock: Optional[int]


class UpdateAuctionRequest(BaseModel):
    id: UUID
    price: Price
    addedKeys: Optional[List[str]]
    acquisitionPrice: Optional[Price]
    removedKeys: Optional[List[str]]
    enabled: Union[bool, str] = False
    autoRenew: Union[bool, str] = False
    lowStockNotificationEnabled: bool = False
    priceChangeNotificationEnabled: bool = False
    declaredStock: Optional[int]


class CountFeeTypeEnum(Enum):
    auction_new = "AUCTION_NEW"
    auction_edit = "AUCTION_EDIT"
    auction_renew = "AUCTION_RENEW"
    wallet_withdraw = "WALLET_WITHDRAW"
    auction_price_update = "AUCTION_PRICE_UPDATE"


class CreateAuctionInDB(ModelMixin):
    auction_id: UUID
    inventory_id: int
