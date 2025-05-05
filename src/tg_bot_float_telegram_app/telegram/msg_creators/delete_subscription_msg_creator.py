from typing import List
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_telegram_app.telegram.msg_creators.command_msg_creator import CommandMsgCreator
from tg_bot_float_telegram_app.tg_constants import (
    DEFAULT_VERSION_TEXT,
    STATTRAK_VERSION_TEXT,
)


class DeleteSubscriptionMsgCreator(CommandMsgCreator):
    async def show_subscriptions_msg(self, subscriptions: List[RelationNameDTO]) -> None:
        lines = ["Выберите подписку для удаления:"]
        lines.extend(
            f'{index + 1}) - "{subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {f"{STATTRAK_VERSION_TEXT}" if subscription.stattrak_existence else f"{DEFAULT_VERSION_TEXT}"}"'
            for index, subscription in enumerate(subscriptions)
        )
        await self._message.answer(text="\n".join(lines))

    async def show_subscription_not_found_msg(self) -> None:
        await self._message.answer(text="Подписка не найдена. Пожалуйста, выберите цифру с нужной вам подпиской выше!.")
