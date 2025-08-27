from pydantic import BaseModel, field_validator
from datetime import  datetime


class PriceBase(BaseModel):
    symbol: str
    currency: str = "USD"
    price: float
    

    @field_validator("symbol")
    @classmethod
    def normalise_symbol(cls, v:str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("symbol cannot be empty")
        return v

class PriceCreate(PriceBase):
    pass

class PriceRead(PriceBase):
    id: int
    fetched_at: datetime