from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.price import PriceCreate, PriceRead
from app.repositories.prices import create_price, list_prices, latest_price, bulk_upsert_prices
from app.db import get_session
from app.services.coingecko import fetch_prices  # the get_session function above

router = APIRouter(prefix="/prices", tags=["prices"])

@router.post("", response_model=PriceRead, status_code=201)
def create_price_endpoint(payload: PriceCreate, db: Session = Depends(get_session)):
    try:
        return create_price(db, **payload.model_dump())
    except Exception as e:
        # You might refine for IntegrityError, etc.
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bulk", status_code=202)
def bulk_ingest_endpoint(payloads: List[PriceCreate], db: Session = Depends(get_session)):
    inserted = bulk_upsert_prices(db, [p.model_dump() for p in payloads])
    return {"inserted": inserted}

@router.get("", response_model=list[PriceRead])
def list_prices_endpoint(
    symbol: str | None = Query(None),
    since: datetime | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
):
    return list_prices(db, symbol=symbol, since=since, limit=limit, offset=offset)

@router.get("/latest/{symbol}", response_model=PriceRead | None)
def latest_price_endpoint(symbol: str, db: Session = Depends(get_session)):
    return latest_price(db, symbol=symbol)

@router.post("/ingest", status_code=202)
def ingest_prices(background: BackgroundTasks, symbols: list[str], db: Session = Depends(get_session)):
    def job():
        rows = fetch_prices(symbols)
        bulk_upsert_prices(db, rows)
    background.add_task(job)
    return {"message": "Ingestion scheduled for: " + ", ".join(symbols)}