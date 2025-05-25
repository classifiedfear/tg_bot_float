from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from redis.asyncio import Redis

from tg_bot_float_telegram_app.service_client.db_app_service_client import DbAppServiceClient


class RegisterCheckMiddleware(BaseMiddleware):
    def __init__(
        self,
        db_app_service_client: DbAppServiceClient,
        redis: Redis,
    ) -> None:
        super().__init__()
        self._db_app_service_client = db_app_service_client
        self._redis = redis

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        await self._redis.delete(str(event.from_user.id))
        if await self._redis.get(str(event.from_user.id)):
            return await handler(event, data)
        if not await self._db_app_service_client.get_user_by_telegram_id(event.from_user.id):
            db_user_id = await self._db_app_service_client.create_user(
                event.from_user.id, str(event.from_user.username), event.from_user.full_name
            )
            await self._redis.set(str(event.from_user.id), db_user_id)
        return await handler(event, data)
