from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.handlers.add_subscription_handler import (
    AddSubscriptionHandler,
)
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.states.add_subscription_states import AddSubscriptionStates
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)


class AddSubscriptionRouterController(AbstractTGRouterController):
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient):
        super().__init__()
        self._hanlder_service = AddSubscriptionHandler(keyboard, db_app_service_client)
        self._init_routes()

    def _init_routes(self):
        self._router.message.register(
            self._start_add_subscription,
            lambda message: message.text == "Отслеживать",
        )
        self._router.message.register(
            self._cancel,
            lambda message: message.text == "Отменить",
        )
        self._router.message.register(
            self._add_subscription_weapon,
            AddSubscriptionStates.CHOOSE_WEAPON,
        )
        self._router.message.register(
            self._add_subscription_skin, AddSubscriptionStates.CHOOSE_SKIN
        )
        self._router.message.register(
            self._add_subscription_quality, AddSubscriptionStates.CHOOSE_QUALITY
        )
        self._router.message.register(self._add_subscription, AddSubscriptionStates.CHOOSE_STATTRAK)

    async def _cancel(self, message: Message, state: FSMContext):
        await self._hanlder_service.cancel(message, state)

    async def _start_add_subscription(self, message: Message, state: FSMContext):
        await self._hanlder_service.start_add_subscription(message, state)

    async def _add_subscription_weapon(self, message: Message, state: FSMContext):
        await self._hanlder_service.add_subscription_weapon(message, state)

    async def _add_subscription_skin(self, message: Message, state: FSMContext):
        await self._hanlder_service.add_subscription_skin(message, state)

    async def _add_subscription_quality(self, message: Message, state: FSMContext):
        await self._hanlder_service.add_subscription_quality(message, state)

    async def _add_subscription(self, message: Message, state: FSMContext):
        await self._hanlder_service.end_add_subscription(message, state)
