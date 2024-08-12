from typing import Any, List

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_common_dtos.schema_dtos.subscription_to_find import SubscriptionToFindDTO
from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_sub_benefit_finder.csm_steam_benefit_finder_settings import (
    CsmSteamBenefitFinderSettings,
)


class SourceDataGetterService:
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(self, settings: CsmSteamBenefitFinderSettings, session: ClientSession) -> None:
        self._settings = settings
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(link, retry_options=self._retry_options) as response:
            return await response.json()

    async def get_user_subscriptions(self) -> List[SubscriptionToFindDTO]:
        subscription_dtos: List[SubscriptionToFindDTO] = []

        current_link: str = self._settings.db_app_base_url + self._settings.user_subscription_url
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._settings.db_app_base_url + next_link_part
            subscription_dtos.extend(
                [SubscriptionToFindDTO.model_validate(item) for item in response_json.get("items")]
            )
        return subscription_dtos

    async def get_weapon_skin_quality_names(
        self, subscription: SubscriptionToFindDTO
    ) -> FullSubscriptionDTO:
        response_json = await self._get_response(
            self._settings.db_app_base_url
            + self._settings.weapon_skin_quality_names_url.format(
                weapon_id=subscription.weapon_id,
                skin_id=subscription.skin_id,
                quality_id=subscription.quality_id,
            )
        )
        return FullSubscriptionDTO(
            weapon_id=subscription.weapon_id,
            skin_id=subscription.skin_id,
            quality_id=subscription.quality_id,
            stattrak=subscription.stattrak,
            weapon_name=response_json["weapon_name"],
            skin_name=response_json["skin_name"],
            quality_name=response_json["quality_name"],
        )

    async def get_csm_items(self, subscription: FullSubscriptionDTO) -> List[CsmItemDTO]:
        csm_items: List[CsmItemDTO] = []
        current_link = self._settings.csm_base_url + self._settings.item_url.format(
            weapon=subscription.weapon_name,
            skin=subscription.skin_name,
            quality=subscription.quality_name,
            stattrak=subscription.stattrak,
        )
        offset = 0
        while True:
            response_json = await self._get_response(current_link + f"?offset={offset}")
            offset += 60
            if isinstance(response_json, dict):
                break
            csm_items.extend([CsmItemDTO.model_validate(item) for item in response_json])
        return csm_items

    async def get_steam_items(self, subscription: FullSubscriptionDTO) -> List[SteamItemDTO]:
        response_json = await self._get_response(
            self._settings.steam_base_url
            + self._settings.item_url.format(
                weapon=subscription.weapon_name,
                skin=subscription.skin_name,
                quality=subscription.quality_name,
                stattrak=subscription.stattrak,
            )
        )
        if isinstance(response_json, dict):
            return []
        return [SteamItemDTO.model_validate(item) for item in response_json]
