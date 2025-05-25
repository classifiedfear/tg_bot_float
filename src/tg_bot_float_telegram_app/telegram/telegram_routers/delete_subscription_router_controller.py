from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.filters import or_f

from tg_bot_float_telegram_app.telegram.constants.general_consts import UNSUB_TEXT
from tg_bot_float_telegram_app.telegram.handlers.delete_subscripton_handler import (
    DeleteSubscriptionHandlerService,
)
from tg_bot_float_telegram_app.telegram.keyboard.buttons import Buttons
from tg_bot_float_telegram_app.telegram.msg_creators.delete_subscription_msg_creator import (
    DeleteSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.state_controllers.delete_subscription_state_controller import (
    DeleteSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)
from tg_bot_float_telegram_app.telegram.states.delete_subscription_states import (
    DeleteSubscriptionStates,
)


class DeleteSubscriptionRouterController(AbstractTGRouterController):
    def __init__(
        self, handler_service: DeleteSubscriptionHandlerService, middleware: BaseMiddleware
    ) -> None:
        super().__init__()
        self._handler_service = handler_service
        self.router.message.middleware(middleware)
        self._init_routes()

    def _init_routes(self) -> None:
        super()._init_routes()
        self._router.message.register(
            self._show_subscriptions,
            lambda message: message.text == UNSUB_TEXT,
        )
        self._router.message.register(
            self._cancel,
            lambda message: message.text == "Отменить",
        )
        self._router.message.register(
            self._delete_subscription,
            DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION,
            or_f(
                lambda message: message.text.isdigit(),
                lambda message: len(message.text.split(",")) == 4,
            ),
        )
        self._router.message.register(
            self._confirm_delete_subscription,
            DeleteSubscriptionStates.CONFIRM_DELETE_SUBSCRIPTION,
            lambda message: message.text.lower().strip() == Buttons.CONFIRM.value.lower(),
        )

    async def _cancel(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await self._handler_service.cancel(msg_creator, state_controller)

    async def _show_subscriptions(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await self._handler_service.show_subscriptions(
            msg_creator, state_controller, message.from_user.id
        )

    async def _delete_subscription(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await self._handler_service.delete_subscription(
            msg_creator, state_controller, message.text, message.from_user.id
        )

    async def _confirm_delete_subscription(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await self._handler_service.confirm_delete_subscription(
            msg_creator, state_controller, message.from_user.id
        )
