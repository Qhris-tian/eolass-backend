from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ActionEnum(Enum):
    provide = "PROVIDE"
    reserve = "RESERVE"
    cancel = "CANCEL"


class TypeEnum(Enum):
    text = "TEXT"
    image = "IMAGE"


class Key(BaseModel):
    type: TypeEnum
    value: str
    filename: Optional[str]


class Auction(BaseModel):
    auctionId: str
    keys: List[Key]


class ReserveRequest(BaseModel):
    action: ActionEnum = ActionEnum.reserve
    orderId: str
    originalOrderId: Optional[str]
    auctions: List
    available: bool = Field(default=True)


class ProvisionRequest(BaseModel):
    action: ActionEnum = ActionEnum.provide
    orderId: str
    originalOrderId: Optional[str]


class ReserveRespone(BaseModel):
    action: ActionEnum = Field(default=ActionEnum.reserve)
    orderId: str
    success: bool
    message: Optional[str]


class ProvisionResponse(BaseModel):
    action: ActionEnum = Field(default=ActionEnum.provide)
    orderId: str
    auctions: List[Auction]
    success: bool
    message: Optional[str]
