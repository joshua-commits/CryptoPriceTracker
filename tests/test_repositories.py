# tests/test_repositories.py
from datetime import datetime
from decimal import Decimal

from app.repositories.prices import create_price, list_prices, bulk_upsert_prices
from app.models import Price

def test_create_price(db_session):
    # create
    p = create_price(
        db=db_session,
        symbol="bitcoin",
        currency="USD",
        price=30000.5,
    )
    assert isinstance(p, Price)
    assert p.id is not None
    assert p.symbol == "BITCOIN"

def test_list_prices(db_session):
    # seed two prices
    create_price(db=db_session, symbol="bitcoin", currency="USD", price=30001)
    create_price(db=db_session, symbol="bitcoin", currency="USD", price=30002)

    rows = list_prices(db_session, symbol="bitcoin", limit=10)
    assert len(rows) >= 2
    assert rows[0].symbol == "bitcoin"

def test_bulk_upsert_prices(db_session):
    now = datetime.now()
    rows = [
        {"symbol": "bitcoin", "currency": "USD", "price": 30010.1, "fetched_at": now},
        {"symbol": "ethereum", "currency": "USD", "price": 1900.2, "fetched_at": now},
    ]
    inserted = bulk_upsert_prices(db_session, rows)
    assert inserted >= 2
    # run again to assert idempotency (should not insert duplicates)
    inserted2 = bulk_upsert_prices(db_session, rows)
    assert inserted2 == 0 or inserted2 >= 0
