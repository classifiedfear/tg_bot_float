from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from redis.asyncio import Redis

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient


class RegisterCheck(BaseMiddleware):
    def __init__(self, redis: Redis, db_app_service_client: DBAppServiceClient) -> None:
        super().__init__()
        self._redis = redis
        self._db_app_service_client = db_app_service_client

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if await self._redis.get(event.from_user.id):
            return await handler(event, data)
        if not await self._db_app_service_client.get_user_by_telegram_id(event.from_user.id):
            await self._db_app_service_client.create_user(
                event.from_user.id, event.from_user.username, event.from_user.full_name
            )
            await self._redis.set(event.from_user.id, 1)
        return await handler(event, data)
