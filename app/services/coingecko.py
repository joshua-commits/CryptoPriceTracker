from datetime import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def fetch_prices(ids: list[str], vs_currency: str = "usd") -> list[dict]:
    result = cg.get_price(ids=",".join(ids), vs_currencies=vs_currency)
    now = datetime.now()
    return [
        {
            "symbol": coin,
            "currency": vs_currency.upper(),
            "price": data.get(vs_currency),
            "fetched_at": now,
        }
        for coin, data in result.items()
    ]
