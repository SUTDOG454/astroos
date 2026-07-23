from datetime import datetime, timezone


def temporal_alignment(event: dict) -> dict:
    """Stable integration contract for AstroOS temporal engines.

    The full Swiss Ephemeris adapter is intentionally downstream of this Phase 2
    boundary. Consumers receive exact UTC timestamps and can add Julian Day,
    planetary state, aspects, midpoints, and harmonics without changing market
    event identity.
    """
    observed = datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
    unix_seconds = observed.timestamp()
    julian_day = unix_seconds / 86400.0 + 2440587.5
    return {
        "event_id": event["event_id"],
        "observed_at_utc": observed.isoformat(),
        "unix_seconds": unix_seconds,
        "julian_day": julian_day,
        "asset_id": event["asset"]["canonical_id"],
        "market": event["market"],
        "astro_state": None,
        "integration_status": "awaiting_swiss_ephemeris",
    }
