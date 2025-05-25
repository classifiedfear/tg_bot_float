import asyncio
from typing import Awaitable, List
from tg_bot_float_common_dtos.schema_dtos.relation_id_dto import RelationIdDTO
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
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

    async def get_subscriptions_by_telegram_id(self, telegram_id: int) -> List[RelationNameDTO]:
        get_subscriptions_url = (
            self._settings.db_app_base_url
            + self._settings.get_subscriptions_by_telegram_id_url.format(telegram_id=telegram_id)
        )
        tasks: List[Awaitable[RelationNameDTO]] = []
        response_json = await self._get_json_response(get_subscriptions_url)
        subs = response_json.get("items")
        for sub in subs:
            sub_dto = SubscriptionDTO.model_validate(sub)
            task = asyncio.create_task(self._get_relation_name_dto(sub_dto))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def _get_relation_name_dto(self, sub_dto: SubscriptionDTO) -> RelationNameDTO:
        url = (
            self._settings.db_app_base_url
            + self._settings.get_weapon_skin_quality_names_url.format(
                weapon_id=sub_dto.weapon_id,
                skin_id=sub_dto.skin_id,
                quality_id=sub_dto.quality_id,
            )
        )
        response_json = await self._get_json_response(url)
        response_json["stattrak_existence"] = sub_dto.stattrak
        return RelationNameDTO.model_validate(response_json)

    async def delete_subscription(self, user_id: int, sub: RelationNameDTO) -> None:
        get_ids_url = (
            self._settings.db_app_base_url
            + self._settings.get_weapon_skin_quality_ids_url.format(
                weapon_name=sub.weapon_name,
                skin_name=sub.skin_name,
                quality_name=sub.quality_name,
            )
        )
        json_response = await self._get_json_response(get_ids_url)
        relation_id_dto = RelationIdDTO.model_validate(json_response)
        delete_sub_url = (
            self._settings.db_app_base_url
            + self._settings.delete_subscription_url.format(
                telegram_id=user_id,
                weapon_id=relation_id_dto.weapon_id,
                skin_id=relation_id_dto.skin_id,
                quality_id=relation_id_dto.quality_id,
                stattrak=sub.stattrak_existence,
            )
        )
        await self._delete_request(delete_sub_url)
