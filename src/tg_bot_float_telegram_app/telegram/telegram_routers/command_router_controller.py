from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.filters import CommandStart

from tg_bot_float_telegram_app.telegram.constants.general_consts import MY_SUBS_TEXT
from tg_bot_float_telegram_app.telegram.handlers.command_handler_service import (
    CommandHandlerService,
)

from tg_bot_float_telegram_app.telegram.msg_creators.command_msg_creator import CommandMsgCreator
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)


class CommandRouterController(AbstractTGRouterController):
    def __init__(
        self,
        command_handler: CommandHandlerService,
        middleware: BaseMiddleware,
        outer_middleware: BaseMiddleware,
    ):
        super().__init__()
        self._router.message.outer_middleware(outer_middleware)
        self._router.message.middleware(middleware)
        self._command_handler = command_handler
        self._init_routes()

    def _init_routes(self):
        self._router.message.register(self._command_start, CommandStart())
        self._router.message.register(
            self._show_subscriptions, lambda message: message.text == MY_SUBS_TEXT
        )

    async def _command_start(self, message: Message, msg_creator: CommandMsgCreator) -> None:
        await self._command_handler.command_start(msg_creator)

    async def _show_subscriptions(self, message: Message, msg_creator: CommandMsgCreator) -> None:
        await self._command_handler.show_subscriptions(msg_creator, message.from_user.id)
