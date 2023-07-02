from enum import Enum
from typing import List

from pydantic import BaseModel


class CallbackType(Enum):
    reserve = "DECLARED_STOCK_RESERVATION"
    provision = "DECLARED_STOCK_PROVISION"
    cancel = "DECLARED_STOCK_CANCELLATION"


class Currency(BaseModel):
    currency: str
    symbol: str
    code: str


class AccountBalance(BaseModel):
    currency: Currency
    balance: float


class AccountBalanceResponse(BaseModel):
    balance: List[AccountBalance]


class RegisterCallbackRequst(BaseModel):
    type: CallbackType
    authorization: str
    url: str
