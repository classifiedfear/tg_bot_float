from typing import List
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_telegram_app.service_client.base_service_client import BaseServiceClient


class WSQRequestsServiceClientMixin(BaseServiceClient):
    """
    Mixin class for handling WeaponSkinQuality requests in a Telegram bot service client.
    """

    async def get_weapons(self) -> List[WeaponDTO]:
        weapon_dtos: List[WeaponDTO] = []

        current_link: str = self._settings.db_app_base_url + self._settings.get_weapons_url
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._settings.db_app_base_url + next_link_part
            weapon_dtos.extend(
                [WeaponDTO.model_validate(item) for item in response_json.get("items")]
            )
        return weapon_dtos

    async def get_skins_for_weapon_id(self, weapon_id: int) -> List[SkinDTO]:
        skin_dtos: List[SkinDTO] = []

        current_link: str = (
            self._settings.db_app_base_url
            + self._settings.get_skins_for_weapon_id_url.format(weapon_id=weapon_id)
        )
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._settings.db_app_base_url + next_link_part
            skin_dtos.extend([SkinDTO.model_validate(item) for item in response_json.get("items")])
        return skin_dtos

    async def get_qualities_for_weapon_skin_ids(
        self, weapon_id: int, skin_id: int
    ) -> List[QualityDTO]:
        quality_dtos: List[QualityDTO] = []

        current_link: str = (
            self._settings.db_app_base_url
            + self._settings.get_qualities_for_weapon_skin_ids_url.format(
                weapon_id=weapon_id, skin_id=skin_id
            )
        )
        next_link_exist: bool = True

        while next_link_exist:
            response_json = await self._get_json_response(current_link)
            if (next_link_part := response_json.get("links").get("next")) is None:
                next_link_exist = False
            else:
                current_link = self._settings.db_app_base_url + next_link_part
            quality_dtos.extend(
                [QualityDTO.model_validate(item) for item in response_json.get("items")]
            )
        return quality_dtos

    async def get_stattrak_existence_for_skin_id(
        self, weapon_id: int, skin_id: int, quality_id: int
    ) -> bool:
        response_json = await self._get_json_response(
            self._settings.db_app_base_url
            + self._settings.get_stattrak_existence_for_skin_id_url.format(
                weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
            )
        )
        return response_json
