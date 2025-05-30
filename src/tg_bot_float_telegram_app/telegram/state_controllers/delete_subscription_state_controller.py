from typing import Any, Dict, List
from tg_bot_float_common_dtos.schema_dtos.full_sub_dto import FullSubDTO
from tg_bot_float_telegram_app.dtos.subs_data_dto import SubsDataDTO
from tg_bot_float_telegram_app.telegram.constants.general_consts import DEFAULT_VERSION_TEXT
from tg_bot_float_telegram_app.telegram.state_controllers.abstract_state_controller import (
    StateController,
)


class DeleteSubscriptionStateController(StateController):
    async def update_all_subs_for_user(
        self, telegram_id: int, subscriptions: List[FullSubDTO]
    ) -> None:
        telegram_id_str = str(telegram_id)
        name_to_index: Dict[str, int] = {}
        for index, subscription in enumerate(subscriptions):
            key = f"{subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {subscription.stattrak}".lower()
            name_to_index[key] = index
        subs_data_dto = SubsDataDTO(subs=subscriptions, name_to_index=name_to_index)
        await self._context.update_data(
            {
                telegram_id_str: subs_data_dto.model_dump(),
            }
        )

    async def try_get_sub_from_user_msg(self, telegram_id: int, user_msg: str) -> FullSubDTO | None:
        subs_data_dto = await self._get_subs_data_dto(telegram_id)
        if user_msg.isdigit():
            return self._found_sub_by_index(subs_data_dto, int(user_msg))
        return await self._found_sub_by_name(subs_data_dto, user_msg)

    async def _found_sub_by_name(
        self, subs_data_dto: SubsDataDTO, user_msg: str
    ) -> FullSubDTO | None:
        user_msg_split = user_msg.replace('"', "").split(", ")
        user_msg_split[-1] = "false" if user_msg_split[-1] == DEFAULT_VERSION_TEXT else "true"
        user_msg = ", ".join(user_msg_split).replace('"', "")
        index = subs_data_dto.name_to_index.get(user_msg.lower())
        if index is None:
            return None
        return self._found_sub_by_index(subs_data_dto, index)

    def _found_sub_by_index(self, subs_data_dto: SubsDataDTO, index: int) -> FullSubDTO | None:
        return subs_data_dto.subs[int(index) - 1]

    async def _get_subs_data_dto(self, telegram_id: int) -> SubsDataDTO:
        context_data = await self._context.get_data()
        return SubsDataDTO.model_validate(context_data.get(str(telegram_id), {}))

    async def _get_possibly_subs_for_delete(self, telegram_id: str) -> Dict[str, Any]:
        context_data = await self._context.get_data()
        if telegram_id not in context_data:
            return {}
        return context_data[telegram_id]

    async def update_sub_to_delete(self, telegram_id: int, subscription: FullSubDTO) -> None:
        telegram_id_str = str(telegram_id)
        possibly_subs_to_delete = await self._get_possibly_subs_for_delete(telegram_id_str)
        possibly_subs_to_delete.update(sub_to_delete=subscription.model_dump())
        await self._context.update_data({telegram_id_str: possibly_subs_to_delete})

    async def get_sub_to_delete(self, telegram_id: int) -> FullSubDTO:
        posibly_subs_to_delete = await self._get_possibly_subs_for_delete(str(telegram_id))
        return FullSubDTO.model_validate(posibly_subs_to_delete.get("sub_to_delete"))
