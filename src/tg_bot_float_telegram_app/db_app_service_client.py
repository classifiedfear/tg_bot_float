import asyncio
from http import HTTPStatus
from typing import Any, Dict, List

from aiohttp import ClientSession


from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.relation_id_dto import RelationIdDTO
from tg_bot_float_common_dtos.schema_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.user_dto import UserDTO
from tg_bot_float_telegram_app.dtos.add_user_values_dto import AddUserDataValues
from tg_bot_float_telegram_app.tg_settings import TgSettings


class DBAppServiceClient:
    _success_responses = list(range(200, 300))

    def __init__(self, tg_settings: TgSettings) -> None:
        self._tg_settings = tg_settings
        self._session = ClientSession()

    async def close(self) -> None:
        await self._session.close()

    async def create_user(self, telegram_id: int, username: str, full_name: str) -> int:
        create_user_link = self._tg_settings.db_app_base_url + self._tg_settings.create_user_url
        user: Dict[str, Any] = {
            "telegram_id": telegram_id,
            "username": username,
            "full_name": full_name,
        }
        async with self._session.post(create_user_link, json=user) as response:
            if response.status in self._success_responses:
                location_header: str = response.headers["Location"]
                user_id = location_header.removeprefix("/users/id/")
                return int(user_id)
            raise AssertionError("User creation failed, response status: {response.status}")

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO | None:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_user_url.format(telegram_id=telegram_id)
        )
        if not response_json.get("message"):
            return UserDTO.model_validate(response_json)

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

    async def get_stattrak_existence_for_skin_id(
        self, weapon_id: int, skin_id: int, quality_id: int
    ) -> bool:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_stattrak_existence_for_skin_id_url.format(
                weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
            )
        )
        return response_json

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

    async def is_subscription_exists(self, user_data_values: AddUserDataValues) -> bool:
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_subscription_url.format(
                telegram_id=user_data_values.tg_user_id,
                weapon_id=user_data_values.weapon_id,
                skin_id=user_data_values.skin_id,
                quality_id=user_data_values.quality_id,
                stattrak=user_data_values.stattrak,
            )
        )
        if not response_json.get("message"):
            return True
        return False

    async def get_subscriptions_by_telegram_id(self, telegram_id: int) -> List[RelationNameDTO]:
        tasks = []
        response_json = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_subscriptions_by_telegram_id_url.format(telegram_id=telegram_id)
        )
        items = response_json.get("items")
        for item in items:
            subscription = SubscriptionDTO.model_validate(item)
            link = (
                self._tg_settings.db_app_base_url
                + self._tg_settings.get_weapon_skin_quality_names_url.format(
                    weapon_id=subscription.weapon_id,
                    skin_id=subscription.skin_id,
                    quality_id=subscription.quality_id,
                    stattrak_existence=subscription.stattrak,
                )
            )
            task = asyncio.create_task(self._get_json_response(link))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return [RelationNameDTO.model_validate(response) for response in responses]

    async def delete_subscription(self, user_id: int, sub: RelationNameDTO) -> None:
        json_response = await self._get_json_response(
            self._tg_settings.db_app_base_url
            + self._tg_settings.get_weapon_skin_quality_ids_url.format(
                weapon_id=sub.weapon_name,
                skin_id=sub.skin_name,
                quality_id=sub.quality_name,
                stattrak_existence=sub.stattrak_existence,
            )
        )
        relation_id_dto = RelationIdDTO.model_validate(json_response)
        await self._delete_request(
            self._tg_settings.db_app_base_url
            + self._tg_settings.delete_subscription_url.format(
                telegram_id=user_id,
                weapon_id=relation_id_dto.weapon_id,
                skin_id=relation_id_dto.skin_id,
                quality_id=relation_id_dto.quality_id,
                stattrak=relation_id_dto.stattrak_existence,
            )
        )

    async def _get_json_response(self, link: str) -> Any:
        async with self._session.get(link) as response:
            return await response.json()

    async def _delete_request(self, link: str) -> None:
        async with self._session.delete(link) as response:
            assert response.status == HTTPStatus.NO_CONTENT

    async def _post_request(self, link: str, json: Dict[str, Any]) -> None:
        async with self._session.post(link, json=json) as response:
            assert response.status == HTTPStatus.CREATED
