from datetime import datetime, timezone

from crypto_data_os.models import MarketSnapshot
from crypto_data_os.pipeline import normalize, validate


def snapshot(**kwargs):
    return MarketSnapshot(
        provider_id="bitcoin",
        symbol="BTC",
        name="Bitcoin",
        observed_at=datetime(2026, 7, 23, 3, 30, tzinfo=timezone.utc),
        price_usd=100000,
        market_cap_usd=2_000_000_000_000,
        volume_24h_usd=50_000_000_000,
        **kwargs,
    )


def test_valid_snapshot_quality():
    q = validate(snapshot())
    assert q.is_valid
    assert q.quality_score == 1.0


def test_invalid_price_is_rejected():
    q = validate(snapshot(price_usd=-1))
    assert not q.is_valid
    assert "missing_or_invalid_price" in q.warnings


def test_normalization_is_deterministic():
    a = normalize(snapshot())
    b = normalize(snapshot())
    assert a.event_id == b.event_id
    assert a.asset["canonical_id"] == "crypto:bitcoin"
    assert a.event_type == "crypto.market.snapshot"
