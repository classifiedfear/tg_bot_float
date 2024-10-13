import abc
from typing import Any, Dict, List
import re
from http import HTTPStatus

from curl_cffi.requests import AsyncSession
from fake_useragent import UserAgent

from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException


class AbstractPageService(abc.ABC):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        self._settings = settings

    @property
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    def _get_item_names(self, regex_pattern: re.Pattern[str], response_text: str) -> List[str]:
        return [match.group(1) for match in regex_pattern.finditer(response_text)]

    async def _get_response(self, link: str) -> str:
        async with AsyncSession() as session:
            response = await session.get(link, headers=self._headers)
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise CsgoDbException("Item with this name not found!")
            return response.text
