from aiogram import html
from aiogram.types import Message
from aiogram.filters import CommandStart

from tg_bot_float_telegram_app.telegram.midlewares.register_check import RegisterCheck
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard


class CommandRouterController(AbstractRouterController):
    def __init__(self, keyboard: Keyboard, register_check: RegisterCheck):
        super().__init__()
        self._keyboard = keyboard
        self._router.message.middleware(register_check)
        self._init_routes()

    def _init_routes(self):
        self._router.message.register(self._command_start, CommandStart())

    async def _command_start(self, message: Message) -> None:
        await message.answer(
            text=f"Привет, {html.bold(str(message.from_user.full_name))}!",
            reply_markup=self._keyboard.main_buttons,
        )
