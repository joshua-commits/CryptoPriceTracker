# script called every 5 minutes 
from app.services.coingecko import fetch_prices
from app.db import SessionLocal
from app.repositories.prices import bulk_upsert_prices


def main():
    symbols = ["bitcoin", "ethereum"]
    rows = fetch_prices(symbols)
    with SessionLocal() as db:
        inserted = bulk_upsert_prices(db, rows)
    print(f"Ingested {inserted} price records for {', '.join(symbols)}")

if __name__ == "__main__":
    main()