from typing import Any, Dict, List
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_telegram_app.dtos.delete_user_values_dto import DeleteUserDataValues
from tg_bot_float_telegram_app.telegram.state_controllers.abstract_state_controller import (
    StateController,
)


class DeleteSubscriptionStateController(StateController):
    async def update_all_subscriptions_for_user(
        self, telegram_id: int, subscriptions: List[RelationNameDTO]
    ) -> None:
        telegram_id_str = str(telegram_id)
        subs = {
            str(index + 1): subscription.model_dump()
            for index, subscription in enumerate(subscriptions)
        }
        await self._context.update_data({telegram_id_str: subs})

    async def try_get_subscription_from_user_msg(
        self, telegram_id: int, user_index: int
    ) -> RelationNameDTO | None:
        telegram_id_str = str(telegram_id)
        subs = await self._get_subscriptions_for_user(telegram_id_str)
        if subs and str(user_index) in subs:
            return RelationNameDTO.model_validate(subs[str(user_index)])

    async def _get_subscriptions_for_user(self, telegram_id: str) -> Dict[str, Any]:
        context_data = await self._context.get_data()
        if telegram_id not in context_data:
            return {}
        return context_data[telegram_id]
