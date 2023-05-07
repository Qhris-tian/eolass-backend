from typing import List

from pydantic import BaseModel


class Currency(BaseModel):
    currency: str
    symbol: str
    code: str


class AccountBalance(BaseModel):
    currency: Currency
    balance: float


class AccountBalanceResponse(BaseModel):
    balance: List[AccountBalance]
