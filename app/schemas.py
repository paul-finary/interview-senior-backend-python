from pydantic import BaseModel


class AssetSchema(BaseModel):
    symbol: str
    quantity: float
    price: float
