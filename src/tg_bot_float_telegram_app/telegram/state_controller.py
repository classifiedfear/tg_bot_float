from typing import Any, Dict, List

from aiogram.fsm.context import FSMContext


from tg_bot_float_telegram_app.telegram.states import AddSubscriptionStates

from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO


class AddSubscriptionStateController:
    @staticmethod
    async def update_all_weapons(state: FSMContext, weapons: List[WeaponDTO]) -> None:
        await state.update_data(
            weapons={str(weapon.name).lower(): weapon.model_dump() for weapon in weapons}
        )

    @staticmethod
    async def update_weapon_id_name(state: FSMContext, weapon_dto: WeaponDTO) -> None:
        await state.update_data(weapon_id=weapon_dto.id, weapon_name=weapon_dto.name)

    @staticmethod
    async def update_skin_id_name(state: FSMContext, skin_dto: SkinDTO) -> None:
        await state.update_data(skin_id=skin_dto.id, skin_name=skin_dto.name)

    @staticmethod
    async def update_quality_id_name(state: FSMContext, quality_dto: QualityDTO) -> None:
        await state.update_data(quality_id=quality_dto.id, quality_name=quality_dto.name)

    @staticmethod
    async def update_all_skins(state: FSMContext, skins: List[SkinDTO]) -> None:
        await state.update_data(skins={str(skin.name).lower(): skin.model_dump() for skin in skins})

    @staticmethod
    async def update_all_qualities(state: FSMContext, qualities: List[QualityDTO]) -> None:
        await state.update_data(
            qualities={str(quality.name).lower(): quality.model_dump() for quality in qualities}
        )

    async def try_get_weapon_from_text(self, state: FSMContext, text: str) -> WeaponDTO | None:
        subs_data = await state.get_data()
        weapons = subs_data["weapons"]
        if weapon_data := self._try_get_item_data_by_msg(text, weapons):
            return WeaponDTO.model_validate(weapon_data)

    async def try_get_skin_from_text(self, state: FSMContext, text: str) -> SkinDTO | None:
        subs_data = await state.get_data()
        skins = subs_data["skins"]
        if skin_data := self._try_get_item_data_by_msg(text, skins):
            return SkinDTO.model_validate(skin_data)

    async def try_get_quality_from_text(self, state: FSMContext, text: str) -> QualityDTO | None:
        subs_data = await state.get_data()
        qualities = subs_data["qualities"]
        if quality_data := self._try_get_item_data_by_msg(text, qualities):
            return QualityDTO.model_validate(quality_data)

    async def set_choosing_weapon_state(self, state: FSMContext) -> None:
        await state.set_state(AddSubscriptionStates.CHOOSE_WEAPON)

    async def set_choosing_skin_state(self, state: FSMContext) -> None:
        await state.set_state(AddSubscriptionStates.CHOOSE_SKIN)

    async def set_choosing_quality_state(self, state: FSMContext) -> None:
        await state.set_state(AddSubscriptionStates.CHOOSE_QUALITY)

    async def set_choosing_stattrak_state(self, state: FSMContext) -> None:
        await state.set_state(AddSubscriptionStates.CHOOSE_STATTRAK)

    async def get_weapon_dto(self, state: FSMContext) -> WeaponDTO:
        subs_data = await state.get_data()
        return WeaponDTO.model_validate(
            {"id": subs_data["weapon_id"], "name": subs_data["weapon_name"]}
        )

    async def get_skin_dto(self, state: FSMContext) -> SkinDTO:
        subs_data = await state.get_data()
        return SkinDTO.model_validate({"id": subs_data["skin_id"], "name": subs_data["skin_name"]})

    async def get_quality_dto(self, state: FSMContext) -> QualityDTO:
        subs_data = await state.get_data()
        return QualityDTO.model_validate(
            {"id": subs_data["quality_id"], "name": subs_data["quality_name"]}
        )

    async def get_full_subscription_dto(
        self, state: FSMContext, stattrak: bool
    ) -> FullSubscriptionDTO:
        subs_data = await state.get_data()
        return FullSubscriptionDTO(
            weapon_id=subs_data["weapon_id"],
            skin_id=subs_data["skin_id"],
            quality_id=subs_data["quality_id"],
            weapon_name=subs_data["weapon_name"],
            skin_name=subs_data["skin_name"],
            quality_name=subs_data["quality_name"],
            stattrak=stattrak,
        )

    async def clear_states(self, state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()

    def _try_get_item_data_by_msg(
        self, msg: str, items: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any] | None:
        return items.get(msg.lower().strip())
