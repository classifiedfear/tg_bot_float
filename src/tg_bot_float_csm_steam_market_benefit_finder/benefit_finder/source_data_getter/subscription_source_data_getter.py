from typing import List
from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.abstract_source_data_getter import (
    AbstractSourceDataGetter,
)


class SubscriptionSourceDataGetter(AbstractSourceDataGetter):
    async def get_user_subscriptions(self) -> List[SubscriptionToFindDTO]:
        subscription_dtos: List[SubscriptionToFindDTO] = []

        current_link: str = (
            self._settings.db_app_base_url + self._settings.get_user_subscription_url
        )
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
            + self._settings.get_item_names_for_subscription_url.format(
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
