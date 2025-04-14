from aiogram.types import Message

from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.handlers.add_subscription_handler import (
    AddSubscriptionHandler,
)
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard
from tg_bot_float_telegram_app.telegram.midlewares.prep_middleware import (
    AddSubscriptionPrepMiddleware,
)
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.states.add_subscription_states import AddSubscriptionStates
from tg_bot_float_telegram_app.telegram.states.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)


class AddSubscriptionRouterController(AbstractTGRouterController):
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient):
        super().__init__()
        self._hanlder_service = AddSubscriptionHandler(db_app_service_client)
        self.router.message.middleware(AddSubscriptionPrepMiddleware(keyboard))
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
        self._router.message.register(
            self._add_subscription_stattrak, AddSubscriptionStates.CHOOSE_STATTRAK
        )
        self._router.message.register(
            self._finish_subscription, AddSubscriptionStates.CONFIRM_USER_REQUEST
        )

    async def _cancel(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.cancel(msg_creator, state_controller)

    async def _start_add_subscription(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.start_add_subscription(msg_creator, state_controller)

    async def _add_subscription_weapon(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.add_subscription_weapon(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_skin(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.add_subscription_skin(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_quality(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.add_subscription_quality(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_stattrak(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.add_subscription_stattrak(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _finish_subscription(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._hanlder_service.finish_subscription(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )
