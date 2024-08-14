from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict
from fastapi import FastAPI

from aiogram import Dispatcher, Bot
from aiogram.types import Update
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis


from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.midlewares.register_check import RegisterCheck
from tg_bot_float_telegram_app.telegram.telegram_routers.command_router_controller import (
    CommandRouterController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.delete_subscription_router_controller import (
    DeleteSubscriptionRouterController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.subscription_router_controller import (
    AddSubscriptionRouterController,
)

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.tg_settings import TgSettings


class TgBotFloatApp:
    def __init__(self, settings: TgSettings) -> None:
        self._settings = settings
        self._redis = Redis(host=self._settings.redis_host)
        self._bot = Bot(
            self._settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self._dp = Dispatcher(storage=RedisStorage(self._redis))
        self._db_app_service_client = DBAppServiceClient(self._settings)
        self._keyboard = Keyboard()
        self._init_middlewares()
        self._init_router_controllers()
        self._dp.include_routers(*[controller.router for controller in self._controllers])

    def _init_middlewares(self) -> None:
        self._register_check_middleware = RegisterCheck(self._redis, self._db_app_service_client)

    def _init_router_controllers(self) -> None:
        self._controllers = [
            CommandRouterController(self._keyboard, self._register_check_middleware),
            AddSubscriptionRouterController(self._keyboard, self._db_app_service_client),
            DeleteSubscriptionRouterController(self._keyboard, self._db_app_service_client),
        ]

    @asynccontextmanager
    async def start_bot(self, app: FastAPI) -> AsyncGenerator[None, Any]:
        await self._bot.set_webhook(
            url=self._settings.ngrok_tunnel_url + self._settings.webhook_url,
            allowed_updates=self._dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        yield
        await self._bot.delete_webhook()
        await self._redis.close()

    async def update_feed(self, data: Dict[str, Any]) -> None:
        update = Update.model_validate(data, context={"bot": self._bot})
        await self._dp.feed_update(self._bot, update)

    @property
    def bot(self) -> Bot:
        return self._bot

    @property
    def keyboard(self) -> Keyboard:
        return self._keyboard

    @property
    def db_app_service_client(self) -> DBAppServiceClient:
        return self._db_app_service_client
