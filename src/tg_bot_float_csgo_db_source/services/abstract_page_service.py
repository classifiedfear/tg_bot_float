import abc
from typing import Any, Dict, List
from http import HTTPStatus
import re

from curl_cffi.requests import AsyncSession
from aiohttp import ClientSession
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings




class AbstractPageService(abc.ABC):
    _statuses = {
        x for x in range(100, 600) if x not in list(range(200, 300)) + [HTTPStatus.FORBIDDEN]
    }

    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        self._settings = settings
        self._retry_options = ExponentialRetry(statuses=self._statuses)

    @property
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_item_names(self, link: str, regex_pattern: re.Pattern[str]) -> List[str]:
        response_text = await self._get_response_with_retries(link)
        return [match.group(1) for match in regex_pattern.finditer(response_text)]

    async def _get_response_with_retries(self, link: str) -> str:
        # for _ in range(self._settings.number_of_retries_when_unauthorized):
        #    retry_session = RetryClient(self._session, retry_options=self._retry_options)
        #    async with retry_session.get(link, headers=self._headers) as response:
        #        if response.status == HTTPStatus.FORBIDDEN:
        #            await self._session.close()
        #            self._session = ClientSession()
        #            continue
        #        return await response.text(encoding="utf-8")
        # raise CsgoDbException("Forbidden: Access is denied")
        # session = AsyncSession()
        # response = await session.get(link, headers=self._headers)
        # return response.text
        async with AsyncSession() as session:
            response = await session.get(link, headers=self._headers)
            return response.text
