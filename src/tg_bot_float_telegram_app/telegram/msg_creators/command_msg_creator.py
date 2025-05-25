from typing import List
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_telegram_app.telegram.constants.general_consts import (
    DEFAULT_VERSION_TEXT,
    FULL_SUB_NAME_TEXT,
    GREETINGS_TEXT,
    MY_SUBS_TEXT,
    NO_SUBS_TEXT,
    STATTRAK_VERSION_TEXT,
)
from tg_bot_float_telegram_app.telegram.msg_creators.msg_creator import MsgCreator


class CommandMsgCreator(MsgCreator):
    async def greetings_msg(self) -> None:
        await self._message.answer(
            text=GREETINGS_TEXT.format(user_name=self._message.from_user.full_name),
            reply_markup=self._keyboard_controller.main_buttons,
        )

    async def show_subscriptions_msg(self, subscriptions: List[RelationNameDTO]):
        lines = [
            f"{MY_SUBS_TEXT}:",
        ]
        lines.extend(
            [
                FULL_SUB_NAME_TEXT.format(
                    index=str(index + 1),
                    weapon_name=subscription.weapon_name,
                    skin_name=subscription.skin_name,
                    quality_name=subscription.quality_name,
                    stattrak=(
                        STATTRAK_VERSION_TEXT
                        if subscription.stattrak_existence
                        else DEFAULT_VERSION_TEXT
                    ),
                )
                for index, subscription in enumerate(subscriptions)
            ]
        )
        await self._message.answer(
            text="\n".join(lines), reply_markup=self._keyboard_controller.main_buttons
        )

    async def show_no_subscriptions_msg(self) -> None:
        await self._message.answer(
            text=NO_SUBS_TEXT, reply_markup=self._keyboard_controller.main_buttons
        )
