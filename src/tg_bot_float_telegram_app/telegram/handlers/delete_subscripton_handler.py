import asyncio
from typing import List
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.msg_creator import AddSubscriptionMsgCreator
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.states import DeleteSubscriptionStates


class DeleteSubscriptionHandelr:
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient) -> None:
        self._keyboard = keyboard
        self._db_app_service_client = db_app_service_client

    async def cancel(self, message: Message, state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer("Возвращаю в главное меню", reply_markup=self._keyboard.main_buttons)

    async def show_subscriptions(self, message: Message, state: FSMContext) -> None:
        await state.set_state(DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION)
        subscriptions = await self._db_app_service_client.get_subscriptions_by_telegram_id(
            message.from_user.id
        )
        full_subscription_dtos = await self._get_full_subscription_dtos(subscriptions)
        sub_data_for_state = {
            f"({sub.weapon_name}, {sub.skin_name}, {sub.quality_name}, {sub.stattrak})".lower(): sub.model_dump()
            for sub in full_subscription_dtos
        }

        await state.update_data(sub_data_for_state)
        answer = AddSubscriptionMsgCreator.create_watch_subscription_msg(full_subscription_dtos)
        await message.answer(answer)

    async def _get_full_subscription_dtos(
        self, subscriptions: List[SubscriptionDTO]
    ) -> List[FullSubscriptionDTO]:
        tasks = []
        for sub in subscriptions:
            task = asyncio.create_task(
                self._db_app_service_client.get_weapon_skin_quality_names(sub)
            )
            tasks.append(task)
        dtos: List[FullSubscriptionDTO] = await asyncio.gather(*tasks)
        return dtos

    async def delete_subscription(self, message: Message, state: FSMContext):
        subs_data = await state.get_data()
        subscription_from_state = subs_data.get(str(message.text).strip().lower())
        sub = FullSubscriptionDTO.model_validate(subscription_from_state)
        await self._db_app_service_client.delete_subscription(message.from_user.id, sub)
        await message.answer(
            f"Подписка: ({sub.weapon_name}, {sub.skin_name}, {sub.quality_name}, {sub.stattrak}) - удалена!",
            reply_markup=self._keyboard.main_buttons,
        )
        await state.clear()
