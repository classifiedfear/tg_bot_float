from typing import Dict, List

from tg_bot_float_common_dtos.db_app_dtos.full_sub_dto import FullSubDTO

from tg_bot_float_telegram_app.dtos.sub_dto import SubsDTO
from tg_bot_float_telegram_app.telegram.constants.general_consts import DEFAULT_VERSION_TEXT
from tg_bot_float_telegram_app.telegram.state_controllers.abstract_state_controller import (
    StateController,
)


class DeleteSubscriptionStateController(StateController):
    async def update_all_subs_for_user(
        self, telegram_id: int, subscriptions: List[FullSubDTO]
    ) -> None:
        name_to_index: Dict[str, int] = {
            f"{subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {subscription.stattrak}".lower(): index
            + 1
            for index, subscription in enumerate(subscriptions)
        }
        subs_dto = SubsDTO(subs=subscriptions, name_to_index=name_to_index)
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"subs_dto": subs_dto.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def get_subs_dto(self, telegram_id: int) -> SubsDTO:
        sub_data = await self._get_sub_data(telegram_id)
        return SubsDTO.model_validate(sub_data.get("subs_dto", {}))

    async def _found_sub_by_name(self, subs_data_dto: SubsDTO, user_msg: str) -> FullSubDTO | None:
        user_msg_split = user_msg.split(", ")
        user_msg_split[-1] = (
            "false" if user_msg_split[-1] == DEFAULT_VERSION_TEXT.lower() else "true"
        )
        user_msg = ", ".join(user_msg_split).replace('"', "")
        index = subs_data_dto.name_to_index.get(user_msg)
        if index is None:
            return None
        return subs_data_dto.subs[int(index) - 1]

    def _found_sub_by_index(self, subs_data_dto: SubsDTO, index: int) -> FullSubDTO | None:
        return subs_data_dto.subs[int(index) - 1]

    async def update_sub_to_delete(self, telegram_id: int, subscription: FullSubDTO) -> None:
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"sub_to_delete": subscription.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def get_sub_to_delete(self, telegram_id: int) -> FullSubDTO:
        sub_data = await self._get_sub_data(telegram_id)
        return FullSubDTO.model_validate(sub_data.get("sub_to_delete", {}))
