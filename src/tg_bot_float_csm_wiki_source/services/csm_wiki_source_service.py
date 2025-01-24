import json
from typing import Any, Dict, Self, Set
from http import HTTPStatus


from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_common_dtos.csm_wiki_source_dtos.csm_wiki_dto import CsmWikiDTO
from tg_bot_float_csm_wiki_source.csm_wiki_source_exceptions import CsmWikiSourceExceptions
from tg_bot_float_csm_wiki_source.csm_wiki_source_settings import CsmWikiSourceSettings
from tg_bot_float_csm_wiki_source.services.dtos.graphql_item_data_dto import CsmWikiItemDTO
from tg_bot_float_csm_wiki_source.services.dtos.graphql_response import GraphqlResponse
from tg_bot_float_csm_wiki_source.services.dtos.graphql_csm_wiki_data_dto import (
    CsmWikiGraphqlDTO,
)
from tg_bot_float_csm_wiki_source.csm_wiki_constants import FORBIDDEN_ERROR_MSG


class CsmWikiSourceService:
    def __init__(self, csm_wiki_source_settings: CsmWikiSourceSettings) -> None:
        self._settings = csm_wiki_source_settings
        statuses = self._configure_retry_statuses()
        self._retry_options = ExponentialRetry(statuses=statuses)

    def _configure_retry_statuses(self):
        not_retry_statuses_str = self._settings.not_retry_statuses.split(",")
        not_retry_statuses = set(range(200, 300))
        not_retry_statuses |= {int(x) for x in not_retry_statuses_str}
        statuses = {x for x in range(100, 600) if x not in not_retry_statuses}
        return statuses

    async def __aenter__(self) -> Self:
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

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
        return await self._get_response_with_retries(
            self._settings.base_url + self._settings.graphql_url, graphql_query
        )

    async def _get_response_with_retries(self, link: str, json_data: Dict[str, Any]) -> GraphqlResponse:
        for _ in range(self._settings.number_of_retries_on_http_forbidden):
            retry_session = RetryClient(self._session, retry_options=self._retry_options)
            async with retry_session.post(link, json=json_data) as response:
                if response.status == HTTPStatus.FORBIDDEN:
                    await self._open_new_client_session()
                    continue
                json_response = await response.json()
                return GraphqlResponse.model_validate(json_response)
        return GraphqlResponse(errors=[{"message": FORBIDDEN_ERROR_MSG}])

    async def _open_new_client_session(self) -> None:
        await self._session.close()
        self._session = ClientSession()

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
