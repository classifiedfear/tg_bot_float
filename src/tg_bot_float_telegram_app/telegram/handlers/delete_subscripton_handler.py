from tg_bot_float_telegram_app.telegram.handlers.handler_service import HandlerService
from tg_bot_float_telegram_app.telegram.msg_creators.delete_subscription_msg_creator import (
    DeleteSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.state_controllers.delete_subscription_state_controller import (
    DeleteSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.states.delete_subscription_states import (
    DeleteSubscriptionStates,
)


class DeleteSubscriptionHandlerService(HandlerService):
    async def show_subscriptions(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_id: int,
    ) -> None:
        subscriptions = await self._db_app_service_client.get_subscriptions_by_telegram_id(user_id)
        if not subscriptions:
            await msg_creator.show_no_subscriptions_msg()
            return
        await msg_creator.show_subscriptions_msg(subscriptions)
        await state_controller.update_all_subscriptions_for_user(user_id, subscriptions)
        await state_controller.set_state(DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION)

    async def delete_subscription(
        self,
        user_msg: str,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_id: int,
    ) -> None:
        sub = await state_controller.try_get_subscription_from_user_msg(user_id, int(user_msg))
        if not sub:
            await msg_creator.show_subscription_not_found_msg()
            return
        await self._db_app_service_client.
