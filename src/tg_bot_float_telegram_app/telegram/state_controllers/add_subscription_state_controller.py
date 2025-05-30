from typing import Any, Dict, List


from tg_bot_float_telegram_app.dtos.qualities_data_dto import QualitiesDataDTO
from tg_bot_float_telegram_app.dtos.skins_data_dto import SkinsDataDTO
from tg_bot_float_telegram_app.dtos.sub_to_add_dto import SubToAddDTO
from tg_bot_float_telegram_app.dtos.weapons_data_dto import WeaponsDataDTO
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

    async def create_user_in_state(self, telegram_id: int) -> None:
        await self._context.update_data({str(telegram_id): {}})

    async def update_weapon_dto_for_user(self, telegram_id: int, weapon_dto: WeaponDTO) -> None:
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"weapon_dto": weapon_dto.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_skin_dto_for_user(self, telegram_id: int, skin_dto: SkinDTO) -> None:
        """
        Update the state with the skin ID and name for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            skin_dto (SkinDTO): The skin DTO containing the skin ID and name.
        """
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"skin_dto": skin_dto.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_quality_id_name_for_user(
        self, telegram_id: int, quality_dto: QualityDTO
    ) -> None:
        """
        Update the state with the quality ID and name for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            quality_dto (QualityDTO): The quality DTO containing the quality ID and name.
        """
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"quality_dto": quality_dto.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_stattrak_for_user(self, telegram_id: int, stattrak: bool) -> None:
        """
        Update the state with the stattrak existence for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            stattrak (bool): The stattrak existence to update in the state.

        """
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"stattrak": stattrak})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_all_weapons_for_user(self, telegram_id: int, weapons: List[WeaponDTO]) -> None:
        """
        Update the state with all weapons.

        Args:
            weapons (List[WeaponDTO]): List of weapon DTOs to update in the state.

        """
        name_to_index: Dict[str, int] = {
            str(weapon.name).lower(): index + 1 for index, weapon in enumerate(weapons)
        }
        weapons_data = WeaponsDataDTO(name_to_index=name_to_index, weapons=weapons)
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"weapons_data": weapons_data.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_all_skins_for_user(self, telegram_id: int, skins: List[SkinDTO]) -> None:
        """
        Update the state with all skins.

        Args:
            skins (List[SkinDTO]): List of skin DTOs to update in the state.

        """
        name_to_index: Dict[str, int] = {
            str(skin.name).lower(): index + 1 for index, skin in enumerate(skins)
        }
        skins_data = SkinsDataDTO(name_to_index=name_to_index, skins=skins)
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"skins_data": skins_data.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def update_all_qualities(self, telegram_id: int, qualities: List[QualityDTO]) -> None:
        """
        Update the state with all qualities.

        Args:
            qualities (List[QualityDTO]): List of quality DTOs to update in the state.

        """
        name_to_index: Dict[str, int] = {
            str(quality.name).lower(): index + 1 for index, quality in enumerate(qualities)
        }
        qualities_data = QualitiesDataDTO(name_to_index=name_to_index, qualities=qualities)
        subs_data = await self._get_subs_data(telegram_id)
        subs_data.update({"qualities_data": qualities_data.model_dump()})
        await self._context.update_data({str(telegram_id): subs_data})

    async def try_get_weapon_from_user_msg(
        self, telegram_id: int, user_msg: str
    ) -> WeaponDTO | None:
        if subs_data := await self._get_subs_data(telegram_id):
            weapons_data = WeaponsDataDTO.model_validate(subs_data.get("weapons_data", {}))
            user_msg = self._normalize_text(user_msg)
            if user_msg.isdigit():
                return weapons_data.weapons[int(user_msg) - 1]
            index = weapons_data.name_to_index.get(user_msg)
            if index is None:
                return
            return weapons_data.weapons[index - 1]

    async def try_get_skin_from_user_msg(self, telegram_id: int, user_msg: str) -> SkinDTO | None:
        """
        Try to get the skin DTO from the user's message.

        Args:
            user_msg (str): The user's message.

        Returns:
            SkinDTO | None: The skin DTO if found, otherwise None.
        """
        if subs_data := await self._get_subs_data(telegram_id):
            skins_data = SkinsDataDTO.model_validate(subs_data.get("skins_data", {}))
            user_msg = self._normalize_text(user_msg)
            if user_msg.isdigit():
                return skins_data.skins[int(user_msg) - 1]
            index = skins_data.name_to_index.get(user_msg)
            if index is None:
                return
            return skins_data.skins[index - 1]

    async def try_get_quality_from_user_msg(
        self, telegram_id: int, user_msg: str
    ) -> QualityDTO | None:
        """
        Try to get the quality DTO from the user's message.

        Args:
            user_msg (str): The user's message.

        Returns:
            QualityDTO | None: The quality DTO if found, otherwise None.

        """
        if subs_data := await self._get_subs_data(telegram_id):
            qualities_data = QualitiesDataDTO.model_validate(subs_data.get("qualities_data", {}))
            user_msg = self._normalize_text(user_msg)
            if user_msg.isdigit():
                return qualities_data.qualities[int(user_msg) - 1]
            index = qualities_data.name_to_index.get(user_msg)
            if index is None:
                return
            return qualities_data.qualities[index - 1]

    async def get_weapon_dto_for_user(self, telegram_id: int) -> WeaponDTO:
        """
        Get the weapon DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            WeaponDTO | None: The weapon DTO if found, otherwise None.
        """
        subs_data = await self._get_subs_data(telegram_id)
        return WeaponDTO.model_validate(subs_data.get("weapon_dto", {}))

    async def get_skin_dto_for_user(self, telegram_id: int) -> SkinDTO:
        """
        Get the skin DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            SkinDTO | None: The skin DTO if found, otherwise None.
        """
        subs_data = await self._get_subs_data(telegram_id)
        return SkinDTO.model_validate(subs_data.get("skin_dto", {}))

    async def get_quality_dto_for_user(self, telegram_id: int) -> QualityDTO:
        """
        Get the quality DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            QualityDTO | None: The quality DTO if found, otherwise None.
        """
        subs_data = await self._get_subs_data(telegram_id)
        return QualityDTO.model_validate(subs_data.get("quality_dto", {}))

    async def get_stattrak_for_user(self, telegram_id: int) -> bool:
        """
        Get the stattrak existence for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            bool: The stattrak existence for the user.
        """
        subs_data = await self._get_subs_data(telegram_id)
        return subs_data.get("stattrak", False)

    async def get_sub_to_add_dto_for_user(self, telegram_id: int) -> SubToAddDTO:
        """
        Get the subscription data transfer object for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            SubToAddDTO: The subscription DTO containing all relevant data.
        """
        subs_data = await self._get_subs_data(telegram_id)
        weapon_dto = WeaponDTO.model_validate(subs_data.get("weapon_dto", {}))
        skin_dto = SkinDTO.model_validate(subs_data.get("skin_dto", {}))
        quality_dto = QualityDTO.model_validate(subs_data.get("quality_dto", {}))
        stattrak = subs_data.get("stattrak", False)
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

    async def _get_subs_data(self, telegram_id: int) -> Dict[str, Any]:
        """
        Get the subscription data for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            Dict[str, Any]: The subscription data for the user.
        """
        context_data = await self._context.get_data()
        return context_data.get(str(telegram_id), {})

    def _normalize_text(self, text: str) -> str:
        """
        Normalize the user message by converting it to lowercase, stripping whitespace, and removing quotes.

        Args:
            text (str): The user message to normalize.

        Returns:
            str: The normalized text.
        """
        text = text.lower().strip()
        if '"' in text:
            text = text.replace('"', "")
        return text

    def _try_get_item_data_by_msg(
        self, msg: str, items: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any] | None:
        """
        Try to get item data by message.

        Args:
            msg (str): The message to search for.
            items (Dict[str, Dict[str, Any]]): The dictionary of items to search in.

        Returns:
            Dict[str, Any] | None: The item data if found, otherwise None.
        """
        return items.get(msg.lower().strip().replace('"', ""))
