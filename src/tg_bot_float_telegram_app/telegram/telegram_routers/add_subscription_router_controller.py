from aiogram import F, BaseMiddleware
from aiogram.types import Message


from tg_bot_float_telegram_app.telegram.handlers.add_subscription_handler_service import (
    AddSubscriptionHandlerService,
)

from tg_bot_float_telegram_app.telegram.keyboard.buttons import Buttons
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.states.add_subscription_states import AddSubscriptionStates

from tg_bot_float_telegram_app.telegram.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)


class AddSubscriptionRouterController(AbstractTGRouterController):
    def __init__(
        self,
        handler_service: AddSubscriptionHandlerService,
        middleware: BaseMiddleware,
    ) -> None:
        super().__init__()
        self._handler_service = handler_service
        self.router.message.middleware(middleware)
        self._init_routes()

    def _init_routes(self):
        self._router.message.register(
            self._start_add_subscription,
            F.text.lower().strip() == Buttons.SUB.value.lower(),
        )
        self._router.message.register(
            self._cancel,
            F.text.lower().strip() == Buttons.CANCEL.value.lower(),
        )
        self._router.message.register(
            self._add_subscription_weapon_id,
            AddSubscriptionStates.CHOOSE_WEAPON,
            F.text.isdigit(),
        )
        self._router.message.register(
            self._add_subscription_weapon_user_text,
            AddSubscriptionStates.CHOOSE_WEAPON,
            ~F.text.isdigit(),
        )
        self._router.message.register(
            self._add_subscription_skin_id, AddSubscriptionStates.CHOOSE_SKIN, F.text.isdigit()
        )
        self._router.message.register(
            self._add_subscription_skin_user_text,
            AddSubscriptionStates.CHOOSE_SKIN,
            ~F.text.isdigit(),
        )

        self._router.message.register(
            self._add_subscription_quality_id,
            AddSubscriptionStates.CHOOSE_QUALITY,
            F.text.isdigit(),
        )
        self._router.message.register(
            self._add_subscription_quality_user_text,
            AddSubscriptionStates.CHOOSE_QUALITY,
            ~F.text.isdigit(),
        )
        self._router.message.register(
            self._add_subscription_base,
            AddSubscriptionStates.CHOOSE_STATTRAK,
            F.text.lower().strip() == Buttons.BASE_VERSION.value.lower(),
        )
        self._router.message.register(
            self._add_subscription_stattrak,
            AddSubscriptionStates.CHOOSE_STATTRAK,
            F.text.lower().strip() == Buttons.STATTRAK_VERSION.value.lower(),
        )
        self._router.message.register(
            self._add_subscription_wrong_stattrak,
            AddSubscriptionStates.CHOOSE_STATTRAK,
            F.text.lower().not_in(
                (Buttons.BASE_VERSION.value.lower(), Buttons.STATTRAK_VERSION.value.lower())
            ),
        )
        self._router.message.register(
            self._finish_subscription,
            AddSubscriptionStates.CONFIRM_USER_REQUEST,
            F.text.lower().strip() == Buttons.CONFIRM.value.lower(),
        )

    async def _cancel(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.cancel(msg_creator, state_controller)

    async def _start_add_subscription(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.start_add_subscription(
            msg_creator, state_controller, message.from_user.id
        )

    async def _add_subscription_weapon_id(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ) -> None:
        """
        Handle the case when the user provides a weapon ID.
        """
        await self._handler_service.add_subscription_weapon_id(
            msg_creator, state_controller, int(message.text), message.from_user.id
        )

    async def _add_subscription_weapon_user_text(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        """
        Handle the case when the user provides a weapon name.
        """
        await self._handler_service.add_subscription_weapon_user_text(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_skin_id(
        self,
        message: Message,
        msg_creator: AddSubscriptionHandlerService,
        state_controller: AddSubscriptionStateController,
    ) -> None:
        """
        Handle the case when the user provides a skin ID.
        """
        await self._handler_service.add_subscription_skin_id(
            msg_creator, state_controller, int(message.text), message.from_user.id
        )

    async def _add_subscription_skin_user_text(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        """
        Handle the case when the user provides a skin name.
        """
        await self._handler_service.add_subscription_skin_user_text(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_quality_id(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.add_subscription_quality_id(
            msg_creator, state_controller, int(message.text), message.from_user.id
        )

    async def _add_subscription_quality_user_text(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.add_subscription_quality_user_text(
            msg_creator, state_controller, str(message.text), message.from_user.id
        )

    async def _add_subscription_base(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.add_subscription_stattrak(
            msg_creator, state_controller, message.from_user.id, False
        )

    async def _add_subscription_stattrak(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.add_subscription_stattrak(
            msg_creator, state_controller, message.from_user.id, True
        )

    async def _add_subscription_wrong_stattrak(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.add_subscription_stattrak(
            msg_creator, state_controller, message.from_user.id
        )

    async def _finish_subscription(
        self,
        message: Message,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await self._handler_service.finish_subscription(
            msg_creator, state_controller, message.from_user.id
        )
