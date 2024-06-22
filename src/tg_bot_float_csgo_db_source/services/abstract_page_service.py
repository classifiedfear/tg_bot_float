import abc
from typing import Any, Dict, List

import re

import aiohttp
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings


class AbstractPageService(abc.ABC):

    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        self._settings = settings
        _statuses = {
            x for x in range(100, 600) if str(x) not in self._settings.not_retry_statuses.split(",")
        }
        self._retry_options = ExponentialRetry(statuses=_statuses)

    @property
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_item_names(self, link: str, regex_pattern: re.Pattern[str]) -> List[str]:
        response_text = await self._get_response_with_retries(link)
        return [match.group(1) for match in regex_pattern.finditer(response_text)]

    async def _get_response_with_retries(self, link: str):
        for retry in range(self._settings.retry_when_unauthorized):
            try:
                async with aiohttp.ClientSession() as session:
                    retry_session = RetryClient(session)
                    async with retry_session.get(
                        link, headers=self._headers, retry_options=self._retry_options
                    ) as response:
                        return await response.text(encoding="utf-8")
            except HTTPForbidden:
                if retry == self._settings.retry_when_unauthorized:
                    raise
