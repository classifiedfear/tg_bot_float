from typing import Dict, List


from tg_bot_float_telegram_app.dtos.items_data_dto import ItemsDataDTO
from tg_bot_float_telegram_app.dtos.sub_to_add_dto import SubToAddDTO
from tg_bot_float_telegram_app.telegram.state_controllers.abstract_state_controller import (
    StateController,
)

from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO


class AddSubscriptionStateController(StateController):
    """
    Controller for managing the state of adding a subscription.

    This class provides methods to update and retrieve subscription-related data
    such as weapon, skin, quality, and stattrak information for a specific user.
    """

    async def update_weapon_dto_for_user(self, telegram_id: int, weapon_dto: WeaponDTO) -> None:
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"weapon_dto": weapon_dto.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_skin_dto_for_user(self, telegram_id: int, skin_dto: SkinDTO) -> None:

        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"skin_dto": skin_dto.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_quality_dto_for_user(self, telegram_id: int, quality_dto: QualityDTO) -> None:
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"quality_dto": quality_dto.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_stattrak_for_user(self, telegram_id: int, stattrak: bool) -> None:
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"stattrak": stattrak})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_all_weapons_for_user(self, telegram_id: int, weapons: List[WeaponDTO]) -> None:

        name_to_index: Dict[str, int] = {
            str(weapon.name).lower(): index + 1 for index, weapon in enumerate(weapons)
        }
        weapons_data = ItemsDataDTO(
            name_to_index=name_to_index, items=weapons, len_items=len(weapons)
        )
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"weapons_data": weapons_data.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_all_skins_for_user(self, telegram_id: int, skins: List[SkinDTO]) -> None:

        name_to_index: Dict[str, int] = {
            str(skin.name).lower(): index + 1 for index, skin in enumerate(skins)
        }
        skins_data = ItemsDataDTO(name_to_index=name_to_index, items=skins, len_items=len(skins))
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"skins_data": skins_data.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def update_all_qualities_for_user(
        self, telegram_id: int, qualities: List[QualityDTO]
    ) -> None:
        name_to_index: Dict[str, int] = {
            str(quality.name).lower(): index + 1 for index, quality in enumerate(qualities)
        }
        qualities_data = ItemsDataDTO(
            name_to_index=name_to_index, items=qualities, len_items=len(qualities)
        )
        sub_data = await self._get_sub_data(telegram_id)
        sub_data.update({"qualities_data": qualities_data.model_dump()})
        await self._context.update_data({str(telegram_id): sub_data})

    async def get_weapons_data(self, telegram_id: int) -> ItemsDataDTO[WeaponDTO]:
        sub_data = await self._get_sub_data(telegram_id)
        return ItemsDataDTO[WeaponDTO].model_validate(sub_data.get("weapons_data", {}))

    async def get_skins_data(self, telegram_id: int) -> ItemsDataDTO[SkinDTO]:
        sub_data = await self._get_sub_data(telegram_id)
        return ItemsDataDTO[SkinDTO].model_validate(sub_data.get("skins_data", {}))

    async def get_qualities_data(self, telegram_id: int) -> ItemsDataDTO[QualityDTO]:
        sub_data = await self._get_sub_data(telegram_id)
        return ItemsDataDTO[QualityDTO].model_validate(sub_data.get("qualities_data", {}))

    async def get_weapon_dto_for_user(self, telegram_id: int) -> WeaponDTO:
        sub_data = await self._get_sub_data(telegram_id)
        return WeaponDTO.model_validate(sub_data.get("weapon_dto", {}))

    async def get_skin_dto_for_user(self, telegram_id: int) -> SkinDTO:
        sub_data = await self._get_sub_data(telegram_id)
        return SkinDTO.model_validate(sub_data.get("skin_dto", {}))

    async def get_quality_dto_for_user(self, telegram_id: int) -> QualityDTO:
        sub_data = await self._get_sub_data(telegram_id)
        return QualityDTO.model_validate(sub_data.get("quality_dto", {}))

    async def get_stattrak_for_user(self, telegram_id: int) -> bool:
        sub_data = await self._get_sub_data(telegram_id)
        return sub_data.get("stattrak", False)

    async def get_sub_to_add_dto_for_user(self, telegram_id: int) -> SubToAddDTO:
        sub_data = await self._get_sub_data(telegram_id)
        weapon_dto = WeaponDTO.model_validate(sub_data.get("weapon_dto", {}))
        skin_dto = SkinDTO.model_validate(sub_data.get("skin_dto", {}))
        quality_dto = QualityDTO.model_validate(sub_data.get("quality_dto", {}))
        stattrak = sub_data.get("stattrak", False)
        return SubToAddDTO(
            tg_user_id=telegram_id,
            weapon_id=weapon_dto.id,
            weapon_name=str(weapon_dto.name),
            skin_id=skin_dto.id,
            skin_name=str(skin_dto.name),
            quality_id=quality_dto.id,
            quality_name=str(quality_dto.name),
            stattrak=stattrak,
        )
