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
from tg_bot_float_telegram_app.user_input_cleaner import UserInputCleaner


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
        await state_controller.create_user_in_state(user_id)
        subs = await self._db_app_service_client.get_subscriptions_by_telegram_id(user_id)
        if not subs:
            await msg_creator.show_no_subscriptions_msg()
            return
        await state_controller.update_all_subs_for_user(user_id, subs)
        await state_controller.set_state(DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION)
        await msg_creator.show_subscriptions_msg(subs)

    async def delete_subscription_user_text(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        user_text: str,
        user_id: int,
    ) -> None:
        subs_dto = await state_controller.get_subs_dto(user_id)
        user_text_cleaned = UserInputCleaner.clean(user_text)
        index = subs_dto.name_to_index.get(user_text_cleaned)
        if index:
            sub_index = index - 1
            sub = subs_dto.subs[sub_index]
            await state_controller.update_sub_to_delete(user_id, sub)
            await msg_creator.confirm_delete_subscription_msg(sub)
            await state_controller.set_state(DeleteSubscriptionStates.CONFIRM_DELETE_SUBSCRIPTION)
        else:
            await msg_creator.show_sub_name_not_found_msg()

    async def delete_subscription_id(
        self,
        msg_creator: DeleteSubscriptionMsgCreator,
        state_controller: DeleteSubscriptionStateController,
        index: int,
        user_id: int,
    ) -> None:
        subs_dto = await state_controller.get_subs_dto(user_id)
        if UserInputCleaner.check_on_index(len(subs_dto.subs), index):
            sub_index = index - 1
            sub = subs_dto.subs[sub_index]
            await state_controller.update_sub_to_delete(user_id, sub)
            await msg_creator.confirm_delete_subscription_msg(sub)
            await state_controller.set_state(DeleteSubscriptionStates.CONFIRM_DELETE_SUBSCRIPTION)
        else:
            await msg_creator.show_sub_id_not_found_msg()

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
