from typing import Any, Dict, List


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

    async def _get_or_create_user_in_state(self, telegram_id: str) -> SubToAddDTO:
        context_data = await self._context.get_data()
        if telegram_id not in context_data:
            user_data_values = SubToAddDTO(tg_user_id=int(telegram_id))
            await self._context.update_data({telegram_id: user_data_values.model_dump()})
            return user_data_values
        return SubToAddDTO.model_validate(context_data[telegram_id])

    async def update_weapon_id_name_for_user(self, telegram_id: int, weapon_dto: WeaponDTO) -> None:
        telegram_id_str = str(telegram_id)
        user_data_values = await self._get_or_create_user_in_state(telegram_id_str)
        user_data_values.weapon_id, user_data_values.weapon_name = weapon_dto.id, weapon_dto.name
        await self._context.update_data({telegram_id_str: user_data_values.model_dump()})

    async def update_skin_id_name_for_user(self, telegram_id: int, skin_dto: SkinDTO) -> None:
        """
        Update the state with the skin ID and name for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            skin_dto (SkinDTO): The skin DTO containing the skin ID and name.
        """

        telegram_id_str = str(telegram_id)
        user_data_values = await self._get_or_create_user_in_state(telegram_id_str)
        user_data_values.skin_id, user_data_values.skin_name = skin_dto.id, skin_dto.name
        await self._context.update_data({telegram_id_str: user_data_values.model_dump()})

    async def update_quality_id_name_for_user(
        self, telegram_id: int, quality_dto: QualityDTO
    ) -> None:
        """
        Update the state with the quality ID and name for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            quality_dto (QualityDTO): The quality DTO containing the quality ID and name.
        """
        telegram_id_str = str(telegram_id)
        user_data_values = await self._get_or_create_user_in_state(telegram_id_str)
        user_data_values.quality_id, user_data_values.quality_name = (
            quality_dto.id,
            quality_dto.name,
        )
        await self._context.update_data({telegram_id_str: user_data_values.model_dump()})

    async def update_stattrak_for_user(self, telegram_id: int, stattrak: bool) -> None:
        """
        Update the state with the stattrak existence for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.
            stattrak (bool): The stattrak existence to update in the state.

        """
        telegram_id_str = str(telegram_id)
        user_data_values = await self._get_or_create_user_in_state(telegram_id_str)
        user_data_values.stattrak = stattrak
        await self._context.update_data({telegram_id_str: user_data_values.model_dump()})

    async def update_all_weapons(self, weapons: List[WeaponDTO]) -> None:
        """
        Update the state with all weapons.

        Args:
            weapons (List[WeaponDTO]): List of weapon DTOs to update in the state.

        """
        await self._context.update_data(
            weapons={
                f"{index+1} {str(weapon.name).lower()}": weapon.model_dump()
                for index, weapon in enumerate(weapons)
            }
        )

    async def update_all_skins(self, skins: List[SkinDTO]) -> None:
        """
        Update the state with all skins.

        Args:
            skins (List[SkinDTO]): List of skin DTOs to update in the state.

        """
        await self._context.update_data(
            skins={
                f"{index+1} {str(skin.name).lower()}": skin.model_dump()
                for index, skin in enumerate(skins)
            }
        )

    async def update_all_qualities(self, qualities: List[QualityDTO]) -> None:
        """
        Update the state with all qualities.

        Args:
            qualities (List[QualityDTO]): List of quality DTOs to update in the state.

        """
        await self._context.update_data(
            qualities={
                f"{index+1} {str(quality.name).lower()}": quality.model_dump()
                for index, quality in enumerate(qualities)
            }
        )

    async def try_get_weapon_from_user_msg(self, user_msg: str) -> WeaponDTO | None:
        subs_data = await self._context.get_data()
        weapons: Dict[str, Any] = subs_data["weapons"]
        user_msg = self._normalize_text(user_msg)
        for name, model in weapons.items():
            if user_msg in name:
                return WeaponDTO.model_validate(model)

    async def try_get_skin_from_user_msg(self, user_msg: str) -> SkinDTO | None:
        """
        Try to get the skin DTO from the user's message.

        Args:
            user_msg (str): The user's message.

        Returns:
            SkinDTO | None: The skin DTO if found, otherwise None.
        """
        subs_data = await self._context.get_data()
        skins: Dict[str, Any] = subs_data["skins"]
        user_msg = self._normalize_text(user_msg)
        for name, model in skins.items():
            if user_msg in name:
                return SkinDTO.model_validate(model)

    async def try_get_quality_from_user_msg(self, user_msg: str) -> QualityDTO | None:
        """
        Try to get the quality DTO from the user's message.

        Args:
            user_msg (str): The user's message.

        Returns:
            QualityDTO | None: The quality DTO if found, otherwise None.

        """
        subs_data = await self._context.get_data()
        qualities: Dict[str, Any] = subs_data["qualities"]
        user_msg = self._normalize_text(user_msg)
        for name, model in qualities.items():
            if user_msg in name:
                return QualityDTO.model_validate(model)

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

    async def get_weapon_dto(self, telegram_id: int) -> WeaponDTO:
        """
        Get the weapon DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            WeaponDTO: The weapon DTO containing the weapon ID and name.

        """
        user_data_values = await self._get_or_create_user_in_state(str(telegram_id))
        return WeaponDTO.model_validate(
            {"id": user_data_values.weapon_id, "name": user_data_values.weapon_name}
        )

    async def get_skin_dto(self, telegram_id: int) -> SkinDTO:
        """
        Get the skin DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            SkinDTO: The skin DTO containing the skin ID and name.
        """
        user_data_values = await self._get_or_create_user_in_state(str(telegram_id))
        return SkinDTO.model_validate(
            {"id": user_data_values.skin_id, "name": user_data_values.skin_name}
        )

    async def get_quality_dto(self, telegram_id: int) -> QualityDTO:
        """
        Get the quality DTO for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            QualityDTO: The quality DTO containing the quality ID and name.
        """
        user_data_values = await self._get_or_create_user_in_state(str(telegram_id))
        return QualityDTO.model_validate(
            {"id": user_data_values.quality_id, "name": user_data_values.quality_name}
        )

    async def get_stattrak(self, telegram_id: int) -> bool:
        user_data_values = await self._get_or_create_user_in_state(str(telegram_id))
        return user_data_values.stattrak

    async def get_user_data_values(
        self,
        telegram_id: int,
    ) -> SubToAddDTO:
        return await self._get_or_create_user_in_state(str(telegram_id))

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
