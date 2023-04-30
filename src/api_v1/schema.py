from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import BaseConfig, BaseModel, Field


class PyObjectId(ObjectId):  # pragma: no cover
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class RWModel(DateTimeModelMixin):
    class Config(BaseConfig):  # pragma: no cover
        allow_population_by_alias = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }


class ModelMixin(RWModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
