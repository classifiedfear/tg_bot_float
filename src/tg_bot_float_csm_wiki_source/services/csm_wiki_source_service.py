import json
from typing import Any, Dict, Set
from http import HTTPStatus


import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_csm_wiki_source.csm_wiki_source_settings import CsmWikiSourceSettings
from tg_bot_float_csm_wiki_source.services.csm_wiki_skin_data_dto import CSMWikiSkinDataDTO


class CsmWikiSourceService:

    def __init__(self, csm_wiki_source_settings: CsmWikiSourceSettings) -> None:
        self._settings = csm_wiki_source_settings
        self._statuses = {
            x for x in range(100, 600) if str(x) not in self._settings.statuses.split(",")
        }
        self._retry_options = ExponentialRetry(statuses=self._statuses)

    async def get_csm_wiki_skin_data(self, weapon: str, skin: str) -> CSMWikiSkinDataDTO:
        data_from_page = await self._get_response_with_retries(weapon, skin)
        return self._get_csm_wiki_skin_data_dto(data_from_page)

    async def _get_response_with_retries(self, weapon: str, skin: str) -> Dict[str, Any] | None:
        get_min_available = self._prep_query(weapon, skin)
        for retry in range(self._settings.retry_numbers):
            async with aiohttp.ClientSession() as session:
                retry_session = RetryClient(session)
                async with retry_session.post(
                    self._settings.base_url + self._settings.graphql_url,
                    json=get_min_available,
                ) as response:
                    if (
                        retry < self._settings.retry_numbers
                        and response.status == HTTPStatus.FORBIDDEN
                    ):
                        continue
                    response_text = await response.text()
                    json_response = json.loads(response_text)
                    return json_response["data"]["get_min_available"]

    def _get_csm_wiki_skin_data_dto(
        self, data_from_page: Dict[str, Any] | None
    ) -> CSMWikiSkinDataDTO:
        qualities: Set[str] = set()
        stattrak_existence = False
        if data_from_page:
            for item in data_from_page:
                if item["isStatTrack"]:
                    stattrak_existence = True
                name = item["name"]
                quality = name.split("(")[-1]
                qualities.add(quality[:-1])
        else:
            return CSMWikiSkinDataDTO()
        return CSMWikiSkinDataDTO(qualities=list(qualities), stattrak_existence=stattrak_existence)

    def _prep_query(self, weapon: str, skin: str) -> Dict[str, Any]:
        graphql_query = json.loads(self._settings.graphql_query, strict=False)
        graphql_query["variables"]["name"] = f"{weapon} | {skin}"
        return graphql_query
