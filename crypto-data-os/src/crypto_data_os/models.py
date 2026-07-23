from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class MarketSnapshot(BaseModel):
    model_config = ConfigDict(extra="ignore")

    provider: str = "coingecko"
    provider_id: str
    symbol: str
    name: str
    observed_at: datetime
    price_usd: float | None = None
    market_cap_usd: float | None = None
    volume_24h_usd: float | None = None
    high_24h_usd: float | None = None
    low_24h_usd: float | None = None
    change_24h_pct: float | None = None


class Quality(BaseModel):
    is_valid: bool
    quality_score: float = Field(ge=0, le=1)
    warnings: list[str] = Field(default_factory=list)


class CryptoMarketSnapshotEvent(BaseModel):
    event_id: str
    event_type: str = "crypto.market.snapshot"
    schema_version: str = "1.0"
    observed_at: datetime
    ingested_at: datetime
    asset: dict[str, str]
    market: dict[str, Any]
    quality: Quality
    provenance: dict[str, str]


def deterministic_event_id(provider: str, endpoint: str, asset_id: str, timestamp: datetime) -> str:
    value = f"{provider}|{endpoint}|{asset_id}|{timestamp.astimezone(timezone.utc).isoformat()}"
    return sha256(value.encode("utf-8")).hexdigest()
