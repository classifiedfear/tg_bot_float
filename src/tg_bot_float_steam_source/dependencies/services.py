from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from tg_bot_float_steam_source.services.steam_source_service import SteamSourceService
from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings

@lru_cache()
def get_settings() -> SteamSourceSettings:
    return SteamSourceSettings()


STEAM_SOURCE_SETTINGS = Annotated[SteamSourceSettings, Depends(get_settings)]


def get_steam_source_service(settings: STEAM_SOURCE_SETTINGS) -> SteamSourceService:
    return SteamSourceService(settings)


STEAM_SOURCE_SERVICE = Annotated[SteamSourceService, Depends(get_steam_source_service)]
