from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.types import Message


from tg_bot_float_telegram_app.telegram.msg_creators.msg_creator import MsgCreator

from tg_bot_float_telegram_app.telegram.state_controllers.abstract_state_controller import (
    StateController,
)


class PrepMiddleware(BaseMiddleware):
    def __init__(
        self, msg_creator: MsgCreator, state_controller: Optional[StateController] | None = None
    ) -> None:
        super().__init__()
        self._state_controller = state_controller
        self._msg_creator = msg_creator

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if self._state_controller:
            self._state_controller.change_fsm_context(data["state"])
            data["state_controller"] = self._state_controller
        self._msg_creator.change_messager(event)
        data["msg_creator"] = self._msg_creator
        return await handler(event, data)
