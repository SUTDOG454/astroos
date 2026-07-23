#!/usr/bin/env bash
set -euo pipefail

BROKER="${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}"
for topic in \
  crypto.assets.raw \
  crypto.assets.normalized \
  crypto.market.snapshot \
  crypto.market.ohlcv \
  crypto.market.features \
  crypto.market.regimes \
  crypto.data.quality \
  astro.market.alignment
 do
  kafka-topics --bootstrap-server "$BROKER" --create --if-not-exists --topic "$topic" --partitions 3 --replication-factor 1
 done
