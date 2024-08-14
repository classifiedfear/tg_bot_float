from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.handlers.delete_subscripton_handler import (
    DeleteSubscriptionHandelr,
)
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_telegram_app.telegram.states import DeleteSubscriptionStates


class DeleteSubscriptionRouterController(AbstractRouterController):
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient) -> None:
        super().__init__()
        self._handler = DeleteSubscriptionHandelr(keyboard, db_app_service_client)
        self._init_routes()

    def _init_routes(self) -> None:
        super()._init_routes()
        self._router.message.register(
            self._show_subscriptions,
            lambda message: message.text == "Отписаться",
        )
        self._router.message.register(
            self._delete_subscription, DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION
        )

    async def _cancel(self, message: Message, state: FSMContext):
        await self._handler.cancel(message, state)

    async def _show_subscriptions(self, message: Message, state: FSMContext) -> None:
        await self._handler.show_subscriptions(message, state)

    async def _delete_subscription(self, message: Message, state: FSMContext) -> None:
        await self._handler.delete_subscription(message, state)