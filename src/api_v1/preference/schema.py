from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from src.api_v1.schema import ModelMixin


class IntervalEnum(Enum):
    daily = "DAILY"
    monthly = "MONTHLY"
    annual = "ANNUAL"


class SpendingLimit(BaseModel):
    interval: IntervalEnum = Field(default=IntervalEnum.daily.value)
    value: float = Field(..., ge=1.0)


class Preference(BaseModel):
    spending_limits: List[SpendingLimit]
    auction_percentage_selling_price: float = Field(..., ge=0.0, le=1.0)


class CreateAccountPreference(Preference, ModelMixin):
    pass


class UpdateAccountPreference(Preference):
    updated_at = datetime.now()
