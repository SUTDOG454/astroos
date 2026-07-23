import asyncio
from datetime import datetime, timezone

import aiohttp

from .config import Settings


class BackfillClient:
    """Historical CoinGecko market-data foundation with resumable checkpoints supplied by callers."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch_range(self, asset_id: str, start: datetime, end: datetime) -> list[dict]:
        params = {
            "vs_currency": self.settings.coingecko_currency,
            "from": int(start.astimezone(timezone.utc).timestamp()),
            "to": int(end.astimezone(timezone.utc).timestamp()),
        }
        headers = {"accept": "application/json"}
        if self.settings.coingecko_api_key:
            headers["x-cg-api-key"] = self.settings.coingecko_api_key
        timeout = aiohttp.ClientTimeout(total=self.settings.coingecko_timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(f"{self.settings.coingecko_base_url}/coins/{asset_id}/market_chart/range", params=params) as response:
                response.raise_for_status()
                return await response.json()


async def backfill(asset_id: str, start: datetime, end: datetime, settings: Settings) -> list[dict]:
    return await BackfillClient(settings).fetch_range(asset_id, start, end)


if __name__ == "__main__":
    raise SystemExit("Use backfill() from a scheduled worker; checkpointing is managed by the orchestration layer.")
