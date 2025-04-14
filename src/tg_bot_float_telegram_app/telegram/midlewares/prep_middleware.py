from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.states.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)


class AddSubscriptionPrepMiddleware(BaseMiddleware):
    def __init__(self, keyboard: Keyboard) -> None:
        super().__init__()
        self._state_controller = AddSubscriptionStateController()
        self._msg_creator = AddSubscriptionMsgCreator(keyboard)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        self._state_controller.set_fsm_context(data["state"])
        self._msg_creator.set_messager(event)
        data["msg_creator"] = self._msg_creator
        data["state_controller"] = self._state_controller
        return await handler(event, data)
