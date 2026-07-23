# CryptoDataOS — AstroOS Phase 2

Production-oriented CoinGecko ingestion foundation for AstroOS. The Phase 2 development stack provides:

`CoinGecko -> raw provenance -> validation -> canonical normalization -> Kafka -> ClickHouse`

It is intentionally provider-neutral at the canonical contract boundary so additional market providers can be added later without changing downstream AstroOS consumers.

## Scope

- CoinGecko market snapshot ingestion
- Canonical `CryptoMarketSnapshot.v1` events
- Deterministic event IDs for idempotency
- Data-quality validation and quality scoring
- Kafka topic contracts
- ClickHouse persistence
- Prometheus metrics
- Docker Compose development infrastructure
- AstroOS temporal alignment contract
- Unit and integration-test scaffolding
- GitHub Actions CI

## Development

1. Copy `.env.example` to `.env`.
2. Set `COINGECKO_API_KEY` if your CoinGecko plan requires it.
3. Start infrastructure: `docker compose up -d kafka clickhouse prometheus grafana`.
4. Start ingestion: `docker compose up --build ingestion`.
5. Inspect ClickHouse on port `8123`, Prometheus on `9090`, and Grafana on `3000`.

For local testing without a live provider, run `pytest` and use the mocked provider fixture.

## Event contract

The canonical event is versioned under `schemas/crypto_market_snapshot_v1.json`. The event contains market observations, data-quality metadata, and provider provenance. AstroOS consumers should depend on this contract rather than CoinGecko response shapes.

## Architecture

```text
CoinGecko
   |
Provider Adapter
   |
Validation -> Canonical Normalization
   |
Kafka: crypto.market.snapshot
   |
ClickHouse: crypto_market_snapshots
   |
AstroOS temporal alignment bridge
```

Phase 3 can add OHLCV backfill, technical features, KCIL regime features, Swiss Ephemeris alignment, and AstroMarketTensor generation without changing the Phase 2 ingestion boundary.
