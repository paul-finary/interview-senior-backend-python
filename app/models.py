import datetime as dt
from enum import Enum

from pydantic import BaseModel, Field


class Asset(BaseModel):
    class Type(str, Enum):
        STOCK = "stock"
        CRYPTO = "crypto"
        REAL_ESTATE = "real_estate"

    symbol: str
    type: Type
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    last_updated_at: dt.datetime = Field(default_factory=dt.datetime.now)

    @property
    def value(self) -> float:
        return self.quantity * self.price
