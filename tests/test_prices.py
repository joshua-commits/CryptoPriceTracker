def test_create_and_list_prices(client):
    # Create a price
    resp = client.post("/prices", json={
        "symbol": "BTC",
        "currency": "USD",
        "price": "12345.6789",
        "fetched_at": "2025-08-21T12:00:00Z"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["symbol"] == "BTC"

    # List prices
    resp2 = client.get("/prices")
    assert resp2.status_code == 200
    items = resp2.json()
    assert len(items) == 1
    assert items[0]["symbol"] == "BTC"
