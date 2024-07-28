from functools import lru_cache
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends

from tg_bot_float_steam_source.services.steam_source_service import SteamSourceService
from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings


@lru_cache()
def get_settings() -> SteamSourceSettings:
    return SteamSourceSettings()  # type: ignore "Load variables from steam_source_variables.env file"


STEAM_SOURCE_SETTINGS = Annotated[SteamSourceSettings, Depends(get_settings)]


async def get_steam_source_service(
    settings: STEAM_SOURCE_SETTINGS,
) -> AsyncGenerator[SteamSourceService, Any]:
    async with SteamSourceService(settings) as service:
        yield service


STEAM_SOURCE_SERVICE = Annotated[SteamSourceService, Depends(get_steam_source_service)]
