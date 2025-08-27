# tests/test_api.py
from datetime import datetime
from decimal import Decimal

def test_create_price_endpoint(client):
    payload = {
        "symbol": "bitcoin",
        "currency": "USD",
        "price": 3002.73,
        "fetched_at": datetime.now().isoformat() + "Z"
    }
    resp = client.post("/prices", json=payload)
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["symbol"] == "BITCOIN"
    assert "id" in data

def test_list_prices_endpoint(client):
    resp = client.get("/prices?symbol=bitcoin")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
