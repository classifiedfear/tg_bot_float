from typing import List
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_telegram_app.telegram.msg_creators.msg_creator import MsgCreator
from tg_bot_float_telegram_app.tg_constants import (
    DEFAULT_VERSION_TEXT,
    MY_SUBSCRIPTIONS_TEXT,
    NO_SUBSCRIPTIONS_TEXT,
    STATTRAK_VERSION_TEXT,
)


class CommandMsgCreator(MsgCreator):
    async def greetings_msg(self) -> None:
        await self._message.answer(
            text=f"Привет, {self._message.from_user.full_name}!",
            reply_markup=self._keyboard_controller.main_buttons,
        )

    async def show_subscriptions_msg(self, subscriptions: List[RelationNameDTO]):
        lines = [
            f"{MY_SUBSCRIPTIONS_TEXT}:",
        ]
        lines.extend(
            [
                f'{index + 1}) - "{subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {f"{STATTRAK_VERSION_TEXT}" if subscription.stattrak_existence else f"{DEFAULT_VERSION_TEXT}"}"'
                for index, subscription in enumerate(subscriptions)
            ]
        )
        await self._message.answer(
            text="\n".join(lines), reply_markup=self._keyboard_controller.main_buttons
        )

    async def show_no_subscriptions_msg(self) -> None:
        await self._message.answer(
            text=NO_SUBSCRIPTIONS_TEXT, reply_markup=self._keyboard_controller.main_buttons
        )
