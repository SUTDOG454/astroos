from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    coingecko_base_url: str = "https://api.coingecko.com/api/v3"
    coingecko_api_key: str | None = None
    coingecko_currency: str = "usd"
    coingecko_asset_ids: str = "bitcoin,ethereum"
    coingecko_poll_seconds: int = 60
    coingecko_requests_per_minute: int = 30
    coingecko_timeout_seconds: float = 20.0

    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_topic: str = "crypto.market.snapshot"
    kafka_group_id: str = "crypto-data-os"

    clickhouse_host: str = "clickhouse"
    clickhouse_port: int = 8123
    clickhouse_database: str = "crypto"
    clickhouse_user: str = "default"
    clickhouse_password: str = ""

    prometheus_port: int = 8000
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def asset_ids(self) -> list[str]:
        return [x.strip() for x in self.coingecko_asset_ids.split(",") if x.strip()]


settings = Settings()
