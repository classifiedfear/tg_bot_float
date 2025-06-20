from typing import List

from tg_bot_float_common_dtos.db_app_dtos.full_sub_dto import FullSubDTO
from tg_bot_float_telegram_app.telegram.constants.delete_sub_consts import (
    CHOOSING_SUB_FOR_DELETE_TEXT,
    CONFIRM_DELETE_SUB_TEXT,
    SUB_DELETED_TEXT,
    SUB_ID_NOT_FOUND_TEXT,
    SUB_NAME_NOT_FOUND_TEXT,
)
from tg_bot_float_telegram_app.telegram.constants.general_consts import (
    BACK_TO_MAIN_MENU_TEXT,
    DEFAULT_VERSION_TEXT,
    FULL_SUB_NAME_TEXT,
    STATTRAK_VERSION_TEXT,
)
from tg_bot_float_telegram_app.telegram.msg_creators.command_msg_creator import CommandMsgCreator


class DeleteSubscriptionMsgCreator(CommandMsgCreator):
    async def show_cancel_msg(self) -> None:
        await self._message.answer(
            BACK_TO_MAIN_MENU_TEXT, reply_markup=self._keyboard_controller.main_buttons
        )

    async def show_subscriptions_msg(self, subscriptions: List[FullSubDTO]) -> None:
        lines = [
            CHOOSING_SUB_FOR_DELETE_TEXT,
        ]
        lines.extend(
            FULL_SUB_NAME_TEXT.format(
                index=index + 1,
                weapon_name=subscription.weapon_name,
                skin_name=subscription.skin_name,
                quality_name=subscription.quality_name,
                stattrak=(STATTRAK_VERSION_TEXT if subscription.stattrak else DEFAULT_VERSION_TEXT),
            )
            for index, subscription in enumerate(subscriptions)
        )
        await self._message.answer(
            text="\n".join(lines), reply_markup=self._keyboard_controller.back_button
        )

    async def show_sub_id_not_found_msg(self) -> None:
        await self._message.answer(text=SUB_ID_NOT_FOUND_TEXT)

    async def show_sub_name_not_found_msg(self) -> None:
        await self._message.answer(
            text=SUB_NAME_NOT_FOUND_TEXT, reply_markup=self._keyboard_controller.back_button
        )

    async def show_subscription_deleted_msg(self, subscription: FullSubDTO) -> None:
        await self._message.answer(
            text=SUB_DELETED_TEXT.format(
                weapon_name=subscription.weapon_name,
                skin_name=subscription.skin_name,
                quality_name=subscription.quality_name,
                stattrak=(STATTRAK_VERSION_TEXT if subscription.stattrak else DEFAULT_VERSION_TEXT),
            ),
            reply_markup=self._keyboard_controller.main_buttons,
        )

    async def confirm_delete_subscription_msg(self, subscription: FullSubDTO) -> None:
        await self._message.answer(
            text=CONFIRM_DELETE_SUB_TEXT.format(
                weapon_name=subscription.weapon_name,
                skin_name=subscription.skin_name,
                quality_name=subscription.quality_name,
                stattrak=(STATTRAK_VERSION_TEXT if subscription.stattrak else DEFAULT_VERSION_TEXT),
            ),
            reply_markup=self._keyboard_controller.confirm_buttons,
        )
