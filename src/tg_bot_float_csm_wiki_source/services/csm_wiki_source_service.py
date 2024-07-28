import json
from typing import Any, Dict, Self, Set
from http import HTTPStatus


from aiohttp import ClientResponse, ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_csm_wiki_source.csm_wiki_source_exceptions import CsmWikiSourceExceptions
from tg_bot_float_csm_wiki_source.csm_wiki_source_settings import CsmWikiSourceSettings
from tg_bot_float_csm_wiki_source.services.dtos.csm_wiki_skin_data_dto import CSMWikiSkinDataDTO
from tg_bot_float_csm_wiki_source.services.dtos.graphql_csm_wiki_data_dto import (
    GraphqlCsmWikiDataDTO,
)
from tg_bot_float_csm_wiki_source.services.dtos.graphql_item_data_dto import GraphqlItemDataDTO
from tg_bot_float_csm_wiki_source.services.dtos.graphql_response import GraphqlResponse


class CsmWikiSourceService:

    def __init__(self, csm_wiki_source_settings: CsmWikiSourceSettings) -> None:
        self._settings = csm_wiki_source_settings
        statuses = self._configure_not_retry_statuses()
        self._retry_options = ExponentialRetry(statuses=statuses)

    def _configure_not_retry_statuses(self):
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

    async def get_csm_wiki_skin_data(self, weapon: str, skin: str) -> CSMWikiSkinDataDTO:
        graphql_query = self._prep_query(weapon, skin)
        graphql_response = await self._get_response_with_retries(graphql_query)
        if graphql_response.errors:
            raise CsmWikiSourceExceptions(
                ", ".join([item["message"] for item in graphql_response.errors])
            )
        get_min_available_csm_wiki_dto = GraphqlCsmWikiDataDTO.model_validate(graphql_response.data)
        return self._get_csm_wiki_skin_data_dto(get_min_available_csm_wiki_dto)

    async def _get_response_with_retries(self, graphql_query: Dict[str, Any]) -> GraphqlResponse:
        for _ in range(self._settings.number_of_retries_on_http_forbidden):
            retry_session = RetryClient(self._session, retry_options=self._retry_options)
            async with retry_session.post(
                self._settings.base_url + self._settings.graphql_url,
                json=graphql_query,
            ) as response:
                if await self._check_on_forbidden(response):
                    continue
                response_json = await response.json()
                return GraphqlResponse.model_validate(response_json)
        return GraphqlResponse(errors=[{"message": "Forbidden: Access is denied"}])

    async def _check_on_forbidden(self, response: ClientResponse) -> bool:
        if response.status == HTTPStatus.FORBIDDEN:
            await self._session.close()
            self._session = ClientSession()
            return True
        return False

    def _get_csm_wiki_skin_data_dto(
        self, data_from_page: GraphqlCsmWikiDataDTO
    ) -> CSMWikiSkinDataDTO:
        qualities: Set[str] = set()
        stattrak_existence = False

        for item in data_from_page.get_min_available:
            item_data = GraphqlItemDataDTO.model_validate(item)
            if item_data.isStatTrack:
                stattrak_existence = True
            name = item_data.name
            quality = name.split("(")[-1]
            qualities.add(quality[:-1])

        return CSMWikiSkinDataDTO(qualities=list(qualities), stattrak_existence=stattrak_existence)

    def _prep_query(self, weapon: str, skin: str) -> Dict[str, Any]:
        graphql_query = json.loads(self._settings.graphql_query, strict=False)
        graphql_query["variables"]["name"] = f"{weapon} | {skin}"
        return graphql_query
