from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy import DateTime, UniqueConstraint, Numeric,text

from .db import Base

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    currency = Column(String, default="USD")
    price = Column(Numeric(18,8), nullable=False)
    fetched_at = Column(DateTime,  nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    __table_args__ = (UniqueConstraint("symbol", "currency", "fetched_at"),)

