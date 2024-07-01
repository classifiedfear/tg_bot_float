import abc
from typing import Any, Dict, List, Self
from http import HTTPStatus

import re

from aiohttp import ClientSession, TCPConnector
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings


class AbstractPageService(abc.ABC):
    _statuses = {
        x for x in range(100, 600) if x not in list(range(200, 300)) + [HTTPStatus.FORBIDDEN]
    }

    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        self._settings = settings
        self._retry_options = ExponentialRetry(statuses=self._statuses)

    async def __aenter__(self) -> Self:
        self._connector = TCPConnector()
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._connector.close()

    @property
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_item_names(self, link: str, regex_pattern: re.Pattern[str]) -> List[str]:
        response_text = await self._get_response_with_retries(link)
        return [match.group(1) for match in regex_pattern.finditer(str(response_text))]

    async def _get_response_with_retries(self, link: str):
        for retry in range(self._settings.number_of_retries_when_unauthorized):
            try:
                async with ClientSession(
                    connector=self._connector, connector_owner=False
                ) as session:
                    retry_session = RetryClient(session, retry_options=self._retry_options)
                    async with retry_session.get(link, headers=self._headers) as response:
                        return await response.text(encoding="utf-8")
            except HTTPForbidden:
                if retry == self._settings.number_of_retries_when_unauthorized:
                    raise
                self._connector.close()
                self._connector = TCPConnector()
