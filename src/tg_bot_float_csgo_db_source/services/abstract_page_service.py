import abc
from typing import Any, Dict, List
from http import HTTPStatus

import aiohttp
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from settings.csgo_db_source_settings import CsgoDbSourceSettings


class AbstractPageService(abc.ABC):
    _statuses = {
        x
        for x in range(100, 600)
        if x not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.FORBIDDEN]
    }
    _retry_options = ExponentialRetry(statuses=_statuses)
    _settings = CsgoDbSourceSettings()

    @property
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_item_names(self, link: str) -> List[str]:
        response_text = await self._get_response_with_retries(link)
        page = BeautifulSoup(response_text, "lxml")
        items = page.find_all("h3", class_="item-box-header")
        return [item.text.strip() for item in items]

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
