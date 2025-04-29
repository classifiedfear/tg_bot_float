from redis.asyncio import Redis

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient


class HandlerService:
    def __init__(self, db_app_service_client: DBAppServiceClient, redis: Redis) -> None:
        self._db_app_service_client = db_app_service_client
        self._redis = redis
