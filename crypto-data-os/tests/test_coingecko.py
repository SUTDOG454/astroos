from aioresponses import aioresponses

from crypto_data_os.coingecko import CoinGeckoClient
from crypto_data_os.config import Settings


async def test_coingecko_markets_parses_response():
    settings = Settings(coingecko_base_url="https://api.example.test/v3")
    payload = [{
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 100000,
        "market_cap": 2e12,
        "total_volume": 5e10,
        "high_24h": 101000,
        "low_24h": 99000,
        "price_change_percentage_24h": 1.2,
    }]
    with aioresponses() as mocked:
        mocked.get("https://api.example.test/v3/coins/markets", payload=payload)
        rows = await CoinGeckoClient(settings).markets(["bitcoin"])
    assert len(rows) == 1
    assert rows[0].symbol == "BTC"
    assert rows[0].price_usd == 100000
