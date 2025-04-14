from aiogram import html
from aiogram.types import Message
from aiogram.filters import CommandStart
from redis.asyncio import Redis

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.midlewares.register_check import RegisterCheck
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard


class CommandRouterController(AbstractTGRouterController):
    def __init__(self, keyboard: Keyboard, redis: Redis, db_app_service_client: DBAppServiceClient):
        super().__init__()
        self._keyboard = keyboard
        self._router.message.middleware(RegisterCheck(redis, db_app_service_client))
        self._db_app_service_client = db_app_service_client
        self._redis = redis
        self._init_routes()

    def _init_routes(self):
        self._router.message.register(self._command_start, CommandStart())

    async def _command_start(self, message: Message) -> None:
        await message.answer(
            text=f"Привет, {html.bold(str(message.from_user.full_name))}!",
            reply_markup=self._keyboard.main_buttons,
        )

    async def _show_subscriptions(self, message: Message) -> None:
        subscriptions = await self._db_app_service_client.get_subscriptions_by_telegram_id(
            message.from_user.id
        )
        pass
