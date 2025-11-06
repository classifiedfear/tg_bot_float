from typing import Annotated
from functools import lru_cache

from fastapi import Depends

from tg_bot_float_csgo_db_source.settings.request_settings import RequestSettings
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@lru_cache
def get_request_settings():
    return RequestSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"


@lru_cache
def get_scrapper_settings():
    return ParserSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"


REQUEST_SETTINGS = Annotated[RequestSettings, Depends(get_request_settings)]
PARSER_SETTINGS = Annotated[ParserSettings, Depends(get_scrapper_settings)]
