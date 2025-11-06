import abc
import re
from typing import Generator, Generic, TypeVar

from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings

T = TypeVar("T")


class AbstractParser(abc.ABC, Generic[T]):
    def __init__(self, settings: ParserSettings) -> None:
        pass

    @abc.abstractmethod
    def get_parsed_data(self, page_html: str) -> T:
        pass

    def _extract_regex(self, pattern: re.Pattern[str], page_html: str) -> str | None:
        if (match := pattern.search(page_html)) is not None:
            return match.group(1)
        return None

    def _get_iter_info(
        self, pattern: re.Pattern[str], response_text: str
    ) -> Generator[str, None, None]:
        for match in pattern.finditer(response_text):
            yield match.group(1)
