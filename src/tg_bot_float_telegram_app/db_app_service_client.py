from http import HTTPStatus
from typing import Any, Dict, List

from aiohttp import ClientSession


from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.user_dto import UserDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_telegram_app.tg_settings import TgSettings


class DBAppServiceClient:
    _success_responses = list(range(200, 300))

    def __init__(self, tg_settings: TgSettings) -> None:
        self._tg_settings = tg_settings

    async def delete_subscription(self, telegram_id: int, subscription_dto: FullSubscriptionDTO):
        async with ClientSession() as session:
            async with session.delete(
                self._tg_settings.db_app_base_url
                + self._tg_settings.delete_subscription_url.format(
                    telegram_id=telegram_id,
                    weapon_id=subscription_dto.weapon_id,
                    skin_id=subscription_dto.skin_id,
                    quality_id=subscription_dto.quality_id,
                    stattrak=subscription_dto.stattrak,
                )
            ) as response:
                assert response.status == 204

    async def get_weapon_skin_quality_names(self, subscription_dto: SubscriptionDTO):
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_weapon_skin_quality_names_url.format(
                weapon_id=subscription_dto.weapon_id,
                skin_id=subscription_dto.skin_id,
                quality_id=subscription_dto.quality_id,
            )
        )
        relation_name_dto = RelationNameDTO.model_validate(response_json)
        return FullSubscriptionDTO(
            weapon_id=subscription_dto.weapon_id,
            skin_id=subscription_dto.skin_id,
            quality_id=subscription_dto.quality_id,
            stattrak=bool(subscription_dto.stattrak),
            weapon_name=relation_name_dto.weapon_name,
            skin_name=relation_name_dto.skin_name,
            quality_name=relation_name_dto.quality_name,
        )

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO | None:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_user_url.format(telegram_id=telegram_id)
        )
        if response_json:
            return UserDTO.model_validate(response_json)

    async def create_user(self, telegram_id: int, username: str, full_name: str) -> None:
        await self._post_request(
            self._tg_settings.db_app_base_url + self._tg_settings.create_user_url,
            json={
                "telegram_id": telegram_id,
                "username": username,
                "full_name": full_name,
            },
        )

    async def get_weapons(self) -> List[WeaponDTO]:
        weapon_dtos: List[WeaponDTO] = []

        current_link: str = self._tg_settings.db_app_base_url + self._tg_settings.get_weapons_url
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._tg_settings.db_app_base_url + next_link_part
            weapon_dtos.extend(
                [WeaponDTO.model_validate(item) for item in response_json.get("items")]
            )
        return weapon_dtos

    async def get_skins_for_weapon_id(self, weapon_id: int) -> List[SkinDTO]:
        skin_dtos: List[SkinDTO] = []

        current_link: str = (
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_skins_for_weapon_id_url.format(weapon_id=weapon_id)
        )
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._tg_settings.db_app_base_url + next_link_part
            skin_dtos.extend([SkinDTO.model_validate(item) for item in response_json.get("items")])
        return skin_dtos

    async def get_qualities_for_weapon_skin_ids(
        self, weapon_id: int, skin_id: int
    ) -> List[QualityDTO]:
        quality_dtos: List[QualityDTO] = []

        current_link: str = (
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_qualities_for_weapon_skin_ids_url.format(
                weapon_id=weapon_id, skin_id=skin_id
            )
        )
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._tg_settings.db_app_base_url + next_link_part
            quality_dtos.extend(
                [QualityDTO.model_validate(item) for item in response_json.get("items")]
            )
        return quality_dtos

    async def get_stattrak_existence_for_skin_id(self, skin_id: int) -> bool:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_stattrak_existence_for_skin_id_url.format(skin_id=skin_id)
        )
        return response_json["stattrak_existence"]

    async def create_subscription(
        self, user_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool | None
    ) -> None:
        await self._post_request(
            self._tg_settings.db_app_base_url + self._tg_settings.create_subscription_url,
            json={
                "user_id": user_id,
                "weapon_id": weapon_id,
                "skin_id": skin_id,
                "quality_id": quality_id,
                "stattrak": stattrak,
            },
        )

    async def get_subscriptions_by_telegram_id(self, telegram_id: int):
        subscription_dtos: List[SubscriptionDTO] = []

        current_link: str = (
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_subscriptions_by_telegram_id_url.format(telegram_id=telegram_id)
        )
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._tg_settings.db_app_base_url + next_link_part
            subscription_dtos.extend(
                [SubscriptionDTO.model_validate(item) for item in response_json.get("items")]
            )
        return subscription_dtos

    async def get_users_telegram_ids_by_subscription(
        self, subscription_info: FullSubscriptionDTO
    ) -> List[int]:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_users_telegram_ids_by_subscription_url.format(
                weapon_id=subscription_info.weapon_id,
                skin_id=subscription_info.skin_id,
                quality_id=subscription_info.quality_id,
                stattrak=subscription_info.stattrak,
            )
        )
        return response_json

    async def _get_json_response(self, link: str) -> Any:
        async with ClientSession() as session:
            async with session.get(link) as response:
                if response.status in self._success_responses:
                    return await response.json()

    async def _post_request(self, link: str, json: Dict[str, Any]) -> None:
        async with ClientSession() as session:
            async with session.post(link, json=json) as response:
                assert response.status == HTTPStatus.CREATED
