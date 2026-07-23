from datetime import datetime, timezone

from .models import CryptoMarketSnapshotEvent, MarketSnapshot, Quality, deterministic_event_id


def validate(snapshot: MarketSnapshot) -> Quality:
    warnings: list[str] = []
    if snapshot.price_usd is None or snapshot.price_usd < 0:
        warnings.append("missing_or_invalid_price")
    if snapshot.market_cap_usd is None:
        warnings.append("missing_market_cap")
    if snapshot.volume_24h_usd is None:
        warnings.append("missing_volume")
    score = max(0.0, 1.0 - 0.2 * len(warnings))
    return Quality(is_valid=score >= 0.6, quality_score=score, warnings=warnings)


def normalize(snapshot: MarketSnapshot) -> CryptoMarketSnapshotEvent:
    quality = validate(snapshot)
    now = datetime.now(timezone.utc)
    return CryptoMarketSnapshotEvent(
        event_id=deterministic_event_id(snapshot.provider, "coins/markets", snapshot.provider_id, snapshot.observed_at),
        observed_at=snapshot.observed_at,
        ingested_at=now,
        asset={
            "canonical_id": f"crypto:{snapshot.provider_id}",
            "provider": snapshot.provider,
            "provider_id": snapshot.provider_id,
            "symbol": snapshot.symbol,
            "name": snapshot.name,
        },
        market={
            "price_usd": snapshot.price_usd,
            "market_cap_usd": snapshot.market_cap_usd,
            "volume_24h_usd": snapshot.volume_24h_usd,
            "high_24h_usd": snapshot.high_24h_usd,
            "low_24h_usd": snapshot.low_24h_usd,
            "change_24h_pct": snapshot.change_24h_pct,
        },
        quality=quality,
        provenance={
            "source": snapshot.provider,
            "endpoint": "coins/markets",
        },
    )
