from typing import List
from tg_bot_float_common_dtos.db_app_dtos.full_sub_dto import FullSubDTO

from tg_bot_float_telegram_app.service_client.base_service_client import BaseServiceClient


class SubRequestsServiceClientMixin(BaseServiceClient):
    """
    Mixin class to handle sub requests for the Telegram bot.
    """

    async def create_subscription(
        self, user_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool | None
    ) -> None:
        create_subscription_url = (
            self._settings.db_app_base_url + self._settings.create_subscription_url
        )
        await self._post_request(
            create_subscription_url,
            json={
                "user_id": user_id,
                "weapon_id": weapon_id,
                "skin_id": skin_id,
                "quality_id": quality_id,
                "stattrak": stattrak,
            },
        )

    async def is_subscription_exists(
        self, telegram_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool
    ) -> bool:
        url = self._settings.db_app_base_url + self._settings.get_subscription_url.format(
            telegram_id=telegram_id,
            weapon_id=weapon_id,
            skin_id=skin_id,
            quality_id=quality_id,
            stattrak=stattrak,
        )
        response_json = await self._get_json_response(url)
        if not response_json.get("message"):
            return True
        return False

    async def get_subscriptions_by_telegram_id(self, telegram_id: int) -> List[FullSubDTO]:
        get_subscriptions_url = (
            self._settings.db_app_base_url
            + self._settings.get_subscriptions_by_telegram_id_url.format(telegram_id=telegram_id)
        )
        response_json = await self._get_json_response(get_subscriptions_url)
        subs = response_json.get("items")
        return [FullSubDTO.model_validate(sub) for sub in subs]

    async def delete_subscription(self, user_id: int, sub: FullSubDTO) -> None:
        delete_sub_url = (
            self._settings.db_app_base_url
            + self._settings.delete_subscription_url.format(
                telegram_id=user_id,
                weapon_id=sub.weapon_id,
                skin_id=sub.skin_id,
                quality_id=sub.quality_id,
                stattrak=sub.stattrak,
            )
        )
        await self._delete_request(delete_sub_url)
