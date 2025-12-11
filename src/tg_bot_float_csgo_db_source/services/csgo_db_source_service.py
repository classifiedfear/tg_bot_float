from typing import Generic

from tg_bot_float_csgo_db_source.parsers.abstract_parser import T, AbstractParser
from tg_bot_float_csgo_db_source.response_service.csgo_db_response_service import (
    CsgoDbSourceResponseService,
)


class CsgoDbSourceService(Generic[T]):
    def __init__(
        self, response_service: CsgoDbSourceResponseService, parser: AbstractParser[T]
    ) -> None:
        self._response_service = response_service
        self._parser = parser

    async def get_page(self, url: str) -> T:
        page_html = await self._response_service.get_page_html(url)
        return self._parser.get_parsed_data(page_html)
