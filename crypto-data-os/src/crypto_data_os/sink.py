import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
import clickhouse_connect

from .config import settings

log = logging.getLogger("crypto-data-os.sink")


async def run() -> None:
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="crypto-data-os-clickhouse",
        value_deserializer=json.loads,
        auto_offset_reset="earliest",
    )
    client = clickhouse_connect.get_client(
        host=settings.clickhouse_host,
        port=settings.clickhouse_port,
        username=settings.clickhouse_user,
        password=settings.clickhouse_password,
        database=settings.clickhouse_database,
    )
    await consumer.start()
    try:
        async for message in consumer:
            event = message.value
            client.insert(
                "crypto_market_snapshots",
                [[
                    event["event_id"],
                    event["observed_at"],
                    event["ingested_at"],
                    event["asset"]["canonical_id"],
                    event["asset"]["provider_id"],
                    event["asset"]["symbol"],
                    event["asset"]["name"],
                    event["market"].get("price_usd"),
                    event["market"].get("market_cap_usd"),
                    event["market"].get("volume_24h_usd"),
                    event["market"].get("high_24h_usd"),
                    event["market"].get("low_24h_usd"),
                    event["market"].get("change_24h_pct"),
                    event["quality"]["quality_score"],
                    event["quality"]["is_valid"],
                    event["quality"]["warnings"],
                    event["provenance"]["source"],
                    event["provenance"]["endpoint"],
                ]],
                column_names=[
                    "event_id", "observed_at", "ingested_at", "canonical_id", "provider_id", "symbol", "name",
                    "price_usd", "market_cap_usd", "volume_24h_usd", "high_24h_usd", "low_24h_usd",
                    "change_24h_pct", "quality_score", "is_valid", "warnings", "source", "endpoint",
                ],
            )
            log.info("Persisted %s", event["event_id"])
    finally:
        await consumer.stop()
        client.close()


if __name__ == "__main__":
    asyncio.run(run())
