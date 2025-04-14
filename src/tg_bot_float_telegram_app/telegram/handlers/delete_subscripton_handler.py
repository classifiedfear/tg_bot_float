#import asyncio
#from typing import List
#from aiogram.types import Message
#from aiogram.fsm.context import FSMContext
#
#from tg_bot_float_common_dtos.schema_dtos.subscription_dto import UserDataValues
#from tg_bot_float_common_dtos.schema_dtos.subscription_id_dto import SubscriptionIdDTO
#from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
#from tg_bot_float_telegram_app.telegram.msg_creators.delete_subscription_msg_creator import (
#    DeleteSubscriptionMsgCreator,
#)
#from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard
#from tg_bot_float_telegram_app.telegram.states.state_controllers.delete_subscription_state_controller import (
#    DeleteSubscriptionStateController,
#)
#from tg_bot_float_telegram_app.tg_constants import (
#    BACK_TO_MAIN_MENU_TEXT,
#    WRONG_ITEM_NAME_TEXT,
#)
#
#
#class DeleteSubscriptionHandler:
#    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient) -> None:
#        self._keyboard = keyboard
#        self._db_app_service_client = db_app_service_client
#        self._state_controller = DeleteSubscriptionStateController()
#        self._msg_creator = DeleteSubscriptionMsgCreator()
#
#    async def cancel(self, message: Message, state: FSMContext) -> None:
#        await self._state_controller.clear_states(state)
#        await message.answer(BACK_TO_MAIN_MENU_TEXT, reply_markup=self._keyboard.main_buttons)
#
#    async def show_subscriptions(self, message: Message, state: FSMContext) -> None:
#        await self._state_controller.set_choosing_subscription_state(state)
#        subscriptions = await self._db_app_service_client.get_subscriptions_by_telegram_id(
#            message.from_user.id
#        )
#        subscription_dtos = await self._get_subscription_dtos(subscriptions)
#        if not subscription_dtos:
#            await message.answer("У вас нет подписок!", reply_markup=self._keyboard.main_buttons)
#            await self._state_controller.clear_states(state)
#            return
#        await self._state_controller.update_subscriptions(state, subscription_dtos)
#        answer = self._msg_creator.create_watch_subscription_msg(subscription_dtos)
#        await message.answer(answer, reply_markup=self._keyboard.back_button)
#
#    async def _get_subscription_dtos(
#        self, subscriptions: List[SubscriptionIdDTO]
#    ) -> List[UserDataValues]:
#        tasks = []
#        for sub in subscriptions:
#            task = asyncio.create_task(
#                self._db_app_service_client.get_weapon_skin_quality_names(sub)
#            )
#            tasks.append(task)
#        dtos: List[UserDataValues] = await asyncio.gather(*tasks)
#        return dtos
#
#    async def delete_subscription(self, message: Message, state: FSMContext):
#        subscription = await self._state_controller.try_get_subscription_from_text(
#            state, str(message.text)
#        )
#        if subscription:
#            await self._db_app_service_client.delete_subscription(
#                message.from_user.id, subscription
#            )
#            await message.answer(
#                self._msg_creator.create_delete_subscription_msg(subscription),
#                reply_markup=self._keyboard.main_buttons,
#            )
#            await state.clear()
#        else:
#            await message.answer(WRONG_ITEM_NAME_TEXT.format(item="подписки"))
#
