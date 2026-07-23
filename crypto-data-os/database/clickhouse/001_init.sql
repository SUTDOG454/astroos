CREATE DATABASE IF NOT EXISTS crypto;

CREATE TABLE IF NOT EXISTS crypto.crypto_market_snapshots
(
    event_id String,
    observed_at DateTime64(3, 'UTC'),
    ingested_at DateTime64(3, 'UTC'),
    canonical_id String,
    provider_id String,
    symbol LowCardinality(String),
    name String,
    price_usd Nullable(Float64),
    market_cap_usd Nullable(Float64),
    volume_24h_usd Nullable(Float64),
    high_24h_usd Nullable(Float64),
    low_24h_usd Nullable(Float64),
    change_24h_pct Nullable(Float64),
    quality_score Float32,
    is_valid Bool,
    warnings Array(String),
    source LowCardinality(String),
    endpoint LowCardinality(String)
)
ENGINE = ReplacingMergeTree(ingested_at)
PARTITION BY toYYYYMM(observed_at)
ORDER BY (canonical_id, observed_at, event_id);

CREATE TABLE IF NOT EXISTS crypto.crypto_data_quality
(
    observed_at DateTime64(3, 'UTC'),
    canonical_id String,
    quality_score Float32,
    is_valid Bool,
    warnings Array(String)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(observed_at)
ORDER BY (canonical_id, observed_at);
