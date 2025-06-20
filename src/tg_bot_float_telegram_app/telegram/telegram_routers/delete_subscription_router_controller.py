from aiogram import F, BaseMiddleware
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
            F.text.lower().strip() == Buttons.UNSUB.value.lower(),
        )
        self._router.message.register(
            self._cancel,
            F.text.lower().strip() == Buttons.CANCEL.value.lower(),
        )
        self._router.message.register(
            self._delete_subscription_id,
            DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION,
            F.text.isdigit(),
        )
        self._router.message.register(
            self._delete_subscription_user_text,
            DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION,
            F.chat.func(lambda chat: len(chat.text.split()) == 4),
        )
        self._router.message.register(
            self._confirm_delete_subscription,
            DeleteSubscriptionStates.CONFIRM_DELETE_SUBSCRIPTION,
            F.text.lower().strip() == Buttons.CONFIRM.value.lower(),
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

    async def _delete_subscription_id(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await self._handler_service.delete_subscription_id(
            msg_creator, state_controller, int(message.text), message.from_user.id
        )

    async def _delete_subscription_user_text(
        self,
        message: Message,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ):
        """
        Handle the case when the user provides a subscription in text format.
        """
        await self._handler_service.delete_subscription_user_text(
            msg_creator, state_controller, str(message.text), message.from_user.id
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
