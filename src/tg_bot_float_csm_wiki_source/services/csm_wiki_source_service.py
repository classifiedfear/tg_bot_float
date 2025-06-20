import json
from typing import Any, Dict, Self, Set

from curl_cffi.requests import AsyncSession
from fake_useragent import UserAgent

from tg_bot_float_common_dtos.csm_wiki_source_dtos.csm_wiki_dto import CsmWikiDTO
from tg_bot_float_csm_wiki_source.csm_wiki_source_exceptions import CsmWikiSourceExceptions
from tg_bot_float_csm_wiki_source.csm_wiki_source_settings import CsmWikiSourceSettings
from tg_bot_float_csm_wiki_source.services.dtos.graphql_item_data_dto import CsmWikiItemDTO
from tg_bot_float_csm_wiki_source.services.dtos.graphql_response import GraphqlResponse
from tg_bot_float_csm_wiki_source.services.dtos.graphql_csm_wiki_data_dto import (
    CsmWikiGraphqlDTO,
)


class CsmWikiSourceService:
    def __init__(self, csm_wiki_source_settings: CsmWikiSourceSettings) -> None:
        self._settings = csm_wiki_source_settings

    async def __aenter__(self) -> Self:
        self._session = AsyncSession()
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    @property
    def _headers(self) -> Dict[str, Any]:
        headers = json.loads(self._settings.headers)
        headers["user-agent"] = f"{UserAgent.random}"
        return headers

    async def get_weapon_skin_data(self, weapon: str, skin: str) -> CsmWikiDTO:
        graphql_response = await self._get_graphql_response(weapon, skin)
        if graphql_response.errors:
            raise CsmWikiSourceExceptions(
                ", ".join([item["message"] for item in graphql_response.errors])
            )
        csm_wiki_graphql_dto = CsmWikiGraphqlDTO.model_validate(graphql_response.data)
        return self._get_csm_wiki_dto(csm_wiki_graphql_dto)

    def _prep_query(self, weapon: str, skin: str) -> Dict[str, Any]:
        graphql_query = json.loads(self._settings.graphql_query, strict=False)
        graphql_query["variables"]["name"] = f"{weapon} | {skin}"
        return graphql_query

    async def _get_graphql_response(self, weapon: str, skin: str) -> GraphqlResponse:
        graphql_query = self._prep_query(weapon, skin)
        response = await self._session.post(
            self._settings.base_url + self._settings.graphql_url,
            json=graphql_query,
            headers=self._headers,
        )
        return GraphqlResponse.model_validate(response.json())

    def _get_csm_wiki_dto(self, csm_wiki_graphql_dto: CsmWikiGraphqlDTO) -> CsmWikiDTO:
        qualities: Set[str] = set()
        stattrak_existence = False

        for item in csm_wiki_graphql_dto.get_min_available:
            item_data = CsmWikiItemDTO.model_validate(item)
            if item_data.isStatTrack:
                stattrak_existence = True
            name = item_data.name
            quality = name.split("(")[-1]
            qualities.add(quality[:-1])

        return CsmWikiDTO(qualities=list(qualities), stattrak_existence=stattrak_existence)
