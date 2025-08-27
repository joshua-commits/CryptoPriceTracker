#CRUD operations
from datetime import datetime
from decimal import Decimal
from typing import Iterable, Sequence
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models import Price

def create_price(db: Session, *, symbol:str, currency:str, price:Decimal) -> Price:
    obj = Price(symbol=symbol, currency=currency, price=price)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def bulk_upsert_prices(db:Session, rows:Iterable[dict]) -> int:
    # rows: [{"symbol": "...", "currency": "...", "price": 123.4, "fetched_at": dt}, ...]
    stmt = (
        insert(Price)
        .values(list(rows))
        .on_conflict_do_nothing( 
    )
    )
    res = db.execute(stmt)
    db.commit()
    return res.rowcount or 0

def list_prices(
    db: Session, *, symbol: str | None = None, since: datetime | None = None, limit: int = 100, offset: int = 0
) -> Sequence[Price]:
    #Prices of all Crypto
    q = select(Price).order_by(desc(Price.fetched_at)).limit(limit).offset(offset)
    if symbol:
        #Prices of a particular cyptocurrency
        q = q.where(Price.symbol == symbol)
    if since:
        #All prices since a particular time
        q = q.where(Price.fetched_at >= since)
    return db.execute(q).scalars().all()

def latest_price(db: Session, *, symbol: str) -> Price | None:
    q = select(Price).where(Price.symbol == symbol).order_by(desc(Price.fetched_at)).limit(1)
    return db.execute(q).scalars().first()