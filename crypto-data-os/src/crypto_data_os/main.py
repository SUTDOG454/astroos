import asyncio
import json
import logging
import time

from aiokafka import AIOKafkaProducer
from prometheus_client import Counter, start_http_server

from .coingecko import CoinGeckoClient
from .config import settings
from .pipeline import normalize

logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("crypto-data-os")
EVENTS = Counter("crypto_events_ingested_total", "Canonical crypto events emitted")
REJECTED = Counter("crypto_events_rejected_total", "Events rejected by quality gate")


async def run() -> None:
    start_http_server(settings.prometheus_port)
    client = CoinGeckoClient(settings)
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode())
    await producer.start()
    try:
        while True:
            try:
                snapshots = await client.markets(settings.asset_ids)
                for snapshot in snapshots:
                    event = normalize(snapshot)
                    if not event.quality.is_valid:
                        REJECTED.inc()
                        log.warning("Rejected event %s: %s", event.event_id, event.quality.warnings)
                        continue
                    await producer.send_and_wait(settings.kafka_topic, event.model_dump(mode="json"))
                    EVENTS.inc()
                    log.info("Published %s %s", event.asset["symbol"], event.event_id)
            except Exception:
                log.exception("Ingestion cycle failed")
            await asyncio.sleep(settings.coingecko_poll_seconds)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(run())
