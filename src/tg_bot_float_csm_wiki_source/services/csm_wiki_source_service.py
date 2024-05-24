import json
from typing import Any, Dict, Set
from http import HTTPStatus


import aiohttp
from fake_useragent import UserAgent
from aiohttp_retry import ExponentialRetry, RetryClient

from settings.csm_wiki_source_settings import CsmWikiSourceSettings
from tg_bot_float_csm_wiki_source.services.csm_wiki_skin_data_dto import CSMWikiSkinDataDTO


class CsmWikiSurceService:
    _graph_data = {
        "operationName": "get_min_available",
        "variables": {"name": ""},
        "query": "query get_min_available($name: String!) {\n"
        "  get_min_available(name: $name) {\n"
        "    name\nisSouvenir\nisStatTrack\nbestPrice\n"
        "bestSource\nsource {\n      trade {\n        "
        "lowestPrice\n        count\n      }"
        "\n      market {\n        lowestPrice\n        count\n      }\n    }\n  }\n}",
    }
    _statuses = {x for x in range(100, 600) if x not in [200, 404, 403]}
    _retry_options = ExponentialRetry(statuses=_statuses)
    _settings = CsmWikiSourceSettings()

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,ru;q=0.9,en-US;q=0.8",
            "Content-Length": "394",
            "Content-Type": "application/json",
            "Origin": "https://wiki.cs.money",
            "user-agent": f"{UserAgent.random}",
        }

    async def get_csm_wiki_skin_data(self, weapon: str, skin: str):
        data_from_page = await self._get_response_with_retries(weapon, skin)
        return self._get_csm_wiki_skin_data_dto(data_from_page)

    async def _get_response_with_retries(self, weapon: str, skin: str) -> Dict[str, Any] | None:
        get_min_available = self._prep_query(weapon, skin)
        for retry in range(1, 4):
            async with aiohttp.ClientSession() as session:
                retry_session = RetryClient(session)
                async with retry_session.post(
                    self._settings.base_url + self._settings.graphql_url, json=get_min_available
                ) as response:
                    if retry <= 3 and response.status == HTTPStatus.FORBIDDEN:
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

    def _prep_query(self, weapon: str, skin: str):
        get_min_available = self._graph_data
        get_min_available["variables"]["name"] = f"{weapon} | {skin}"
        return get_min_available
