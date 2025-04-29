from typing import List

from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_telegram_app.db_app_service_client import AddUserDataValues
from tg_bot_float_telegram_app.telegram.msg_creators.msg_creator import MsgCreator
from tg_bot_float_telegram_app.tg_constants import (
    ALREADY_SUBSCRIBED_TEXT,
    BACK_TO_MAIN_MENU_TEXT,
    CHOOSE_VARIANTS_TEXT,
    CHOOSING_ITEM_TEXT,
    CHOOSING_STATTRAK_TEXT,
    FULL_CONFIRM_TEXT,
    DEFAULT_VERSION_TEXT,
    LEN_OF_QUALITIES_TEXT,
    LEN_OF_SKINS_TEXT,
    LEN_OF_WEAPONS_TEXT,
    STATTRAK_VERSION_TEXT,
    SUBSCRIBED_TEXT,
    WEAPON_SKIN_NOT_EXIST_TEXT,
    WRONG_ITEM_NAME_TEXT,
)


class AddSubscriptionMsgCreator(MsgCreator):
    async def show_cancel_msg(self) -> None:
        await self._message.answer(BACK_TO_MAIN_MENU_TEXT, reply_markup=self._keyboard_controller.main_buttons)

    async def show_choose_weapon_msg(self, weapons: List[WeaponDTO]) -> None:
        lines = [
            LEN_OF_WEAPONS_TEXT.format(weapon_len=len(weapons)),
            CHOOSING_ITEM_TEXT,
        ]
        lines.extend([f'{index + 1}) - "{weapon.name}"' for index, weapon in enumerate(weapons)])
        await self._message.answer(
            "\n".join(lines),
            reply_markup=self._keyboard_controller.back_button,
        )

    async def show_wrong_item_name_msg(self, item_name: str) -> None:
        await self._message.answer(WRONG_ITEM_NAME_TEXT.format(item=item_name))

    async def show_weapon_skin_not_exist_msg(self) -> None:
        """Show a message indicating that the weapon skin does not exist."""
        await self._message.answer(
            WEAPON_SKIN_NOT_EXIST_TEXT, reply_markup=self._keyboard_controller.main_buttons
        )

    async def show_choose_skin_msg(self, skins: List[SkinDTO]) -> None:
        lines = [
            LEN_OF_SKINS_TEXT.format(skin_len=len(skins)),
            CHOOSING_ITEM_TEXT,
        ]
        lines.extend([f'{index + 1} - "{skin.name}"' for index, skin in enumerate(skins)])
        await self._message.answer("\n".join(lines))

    async def show_choose_quality_msg(self, qualities: List[QualityDTO]) -> None:
        lines = [
            LEN_OF_QUALITIES_TEXT.format(quality_len=len(qualities)),
            CHOOSING_ITEM_TEXT,
        ]
        lines.extend(
            [f'{index + 1} - "{str(quality.name)}"' for index, quality in enumerate(qualities)]
        )
        await self._message.answer("\n".join(lines))

    async def show_choose_stattrak_msg(self) -> None:
        await self._message.answer(
            CHOOSING_STATTRAK_TEXT, reply_markup=self._keyboard_controller.choose_stattrak_buttons
        )

    async def show_choose_variants(self) -> None:
        """
        Show the message to choose variants.
        """
        await self._message.answer(
            CHOOSE_VARIANTS_TEXT,
            reply_markup=self._keyboard_controller.choose_stattrak_buttons,
        )

    async def show_confirm_msg(
        self,
        weapon_dto: WeaponDTO,
        skin_dto: SkinDTO,
        quality_dto: QualityDTO,
        stattrak_existence: bool,
    ) -> None:
        await self._message.answer(
            FULL_CONFIRM_TEXT.format(
                weapon=weapon_dto.name,
                skin=skin_dto.name,
                quality=quality_dto.name,
                stattrak=(STATTRAK_VERSION_TEXT if stattrak_existence else DEFAULT_VERSION_TEXT),
            ),
            reply_markup=self._keyboard_controller.confirm_buttons,
        )

    async def show_already_subscribed_msg(self) -> None:
        await self._message.answer(
            ALREADY_SUBSCRIBED_TEXT, reply_markup=self._keyboard_controller.main_buttons
        )

    async def show_back_to_main_menu_msg(self) -> None:
        await self._message.answer(BACK_TO_MAIN_MENU_TEXT, reply_markup=self._keyboard_controller.main_buttons)

    async def show_subscribed_msg(self, user_data_values: AddUserDataValues) -> None:
        message_text = self._create_subscribed_message(user_data_values)
        await self._message.answer(message_text, reply_markup=self._keyboard_controller.main_buttons)

    def _create_subscribed_message(self, user_data_values: AddUserDataValues) -> str:
        return SUBSCRIBED_TEXT.format(
            weapon_name=user_data_values.weapon_name,
            skin_name=user_data_values.skin_name,
            quality_name=user_data_values.quality_name,
            stattrak=(STATTRAK_VERSION_TEXT if user_data_values.stattrak else DEFAULT_VERSION_TEXT),
        )
