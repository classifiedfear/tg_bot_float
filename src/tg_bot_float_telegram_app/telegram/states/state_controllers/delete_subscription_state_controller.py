from typing import List

from aiogram.fsm.context import FSMContext


from tg_bot_float_telegram_app.telegram.states.delete_subscription_states import (
    DeleteSubscriptionStates,
)
from tg_bot_float_telegram_app.telegram.states.state_controllers.abstract_state_controller import (
    AbstractStateController,
)
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import UserDataValues


class DeleteSubscriptionStateController(AbstractStateController):
    async def set_choosing_subscription_state(self, state: FSMContext) -> None:
        await state.set_state(DeleteSubscriptionStates.CHOOSE_SUBSCRIPTION)

    async def update_subscriptions(
        self, state: FSMContext, subscription_dtos: List[UserDataValues]
    ) -> None:
        sub_data_for_state = {
            f'{sub.weapon_name}, {sub.skin_name}, {sub.quality_name}, {sub.stattrak}'.lower(): sub.model_dump()
            for sub in subscription_dtos
        }
        await state.update_data(sub_data_for_state)

    async def try_get_subscription_from_text(
        self, state: FSMContext, text: str
    ) -> UserDataValues | None:
        subs_data = await state.get_data()
        subscription_from_state = subs_data.get(text.strip().lower().replace('"', ""))
        if subscription_from_state:
            return UserDataValues.model_validate(subscription_from_state)
