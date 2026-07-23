CREATE TABLE IF NOT EXISTS crypto.crypto_features
(
    asset_id String,
    observed_at DateTime64(3, 'UTC'),
    return_1d Nullable(Float64),
    volatility_7d Nullable(Float64),
    drawdown_30d Nullable(Float64),
    momentum_30d Nullable(Float64)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(observed_at)
ORDER BY (asset_id, observed_at);

CREATE TABLE IF NOT EXISTS crypto.crypto_market_regimes
(
    observed_at DateTime64(3, 'UTC'),
    regime LowCardinality(String),
    score Float64,
    methodology_version String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(observed_at)
ORDER BY observed_at;

CREATE TABLE IF NOT EXISTS crypto.astro_market_alignment
(
    event_id String,
    observed_at DateTime64(3, 'UTC'),
    julian_day Float64,
    asset_id String,
    planetary_state_json String,
    alignment_version String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(observed_at)
ORDER BY (asset_id, observed_at, event_id);
