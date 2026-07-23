from datetime import datetime, timezone

from .models import CryptoMarketSnapshotEvent


def freshness_seconds(event: CryptoMarketSnapshotEvent) -> float:
    return max(0.0, (datetime.now(timezone.utc) - event.observed_at).total_seconds())


def quality_status(event: CryptoMarketSnapshotEvent) -> str:
    if not event.quality.is_valid:
        return "REJECTED"
    if event.quality.quality_score < 0.8 or freshness_seconds(event) > 900:
        return "WARNING"
    return "VALID"
