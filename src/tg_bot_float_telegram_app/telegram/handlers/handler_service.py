from redis.asyncio import Redis

from tg_bot_float_telegram_app.service_client.db_app_service_client import DbAppServiceClient


class HandlerService:
    def __init__(self, db_app_service_client: DbAppServiceClient, redis: Redis) -> None:
        self._db_app_service_client = db_app_service_client
        self._redis = redis
