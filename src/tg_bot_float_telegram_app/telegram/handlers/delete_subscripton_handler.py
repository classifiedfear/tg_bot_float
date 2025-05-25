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
    async def cancel(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
    ) -> None:
        await state_controller.clear_states()
        await msg_creator.show_cancel_msg()

    async def show_subscriptions(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_id: int,
    ) -> None:
        subs = await self._db_app_service_client.get_subscriptions_by_telegram_id(user_id)
        if not subs:
            await msg_creator.show_no_subscriptions_msg()
            return
        await state_controller.update_all_subs_for_user(user_id, subs)
        await state_controller.set_state(DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION)
        await msg_creator.show_subscriptions_msg(subs)

    async def delete_subscription(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_msg: str,
        user_id: int,
    ) -> None:
        sub = await state_controller.try_get_sub_from_user_msg(user_id, user_msg)
        if not sub:
            await msg_creator.show_subscription_not_found_msg()
            return
        await state_controller.update_sub_to_delete(user_id, sub)
        await msg_creator.confirm_delete_subscription_msg(sub)
        await state_controller.set_state(DeleteSubscriptionStates.CONFIRM_DELETE_SUBSCRIPTION)

    async def confirm_delete_subscription(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_id: int,
    ) -> None:
        sub = await state_controller.get_sub_to_delete(user_id)
        await self._db_app_service_client.delete_subscription(user_id, sub)
        await msg_creator.show_subscription_deleted_msg(sub)
        await state_controller.clear_states()
