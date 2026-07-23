import asyncio
from datetime import datetime, timezone
from typing import Any

import aiohttp

from .config import Settings
from .models import MarketSnapshot


class CoinGeckoError(RuntimeError):
    pass


class CoinGeckoClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._last_request = 0.0

    async def markets(self, asset_ids: list[str]) -> list[MarketSnapshot]:
        if not asset_ids:
            return []
        params = {
            "vs_currency": self.settings.coingecko_currency,
            "ids": ",".join(asset_ids),
            "price_change_percentage": "24h",
        }
        headers = {"accept": "application/json"}
        if self.settings.coingecko_api_key:
            headers["x-cg-api-key"] = self.settings.coingecko_api_key
        timeout = aiohttp.ClientTimeout(total=self.settings.coingecko_timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            for attempt in range(4):
                try:
                    async with session.get(f"{self.settings.coingecko_base_url}/coins/markets", params=params) as response:
                        if response.status == 429 or response.status >= 500:
                            if attempt == 3:
                                raise CoinGeckoError(f"CoinGecko unavailable: HTTP {response.status}")
                            await asyncio.sleep(2 ** attempt)
                            continue
                        if response.status >= 400:
                            raise CoinGeckoError(f"CoinGecko request failed: HTTP {response.status}")
                        payload: list[dict[str, Any]] = await response.json()
                        now = datetime.now(timezone.utc)
                        return [
                            MarketSnapshot(
                                provider_id=str(item["id"]),
                                symbol=str(item.get("symbol", "")).upper(),
                                name=str(item.get("name", "")),
                                observed_at=now,
                                price_usd=item.get("current_price"),
                                market_cap_usd=item.get("market_cap"),
                                volume_24h_usd=item.get("total_volume"),
                                high_24h_usd=item.get("high_24h"),
                                low_24h_usd=item.get("low_24h"),
                                change_24h_pct=item.get("price_change_percentage_24h"),
                            )
                            for item in payload
                        ]
                except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                    if attempt == 3:
                        raise CoinGeckoError(str(exc)) from exc
                    await asyncio.sleep(2 ** attempt)
        raise CoinGeckoError("Unreachable")
