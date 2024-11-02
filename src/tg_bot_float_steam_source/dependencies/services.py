from functools import lru_cache
from typing import Annotated, Any, AsyncGenerator

from aiohttp import ClientSession
from fastapi import Depends

from tg_bot_float_steam_source.services.float_source_service import FloatSourceService
from tg_bot_float_steam_source.services.steam_market_source_service import SteamMarketSourceService
from tg_bot_float_steam_source.services.steam_source_service import SteamSourceService
from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings


@lru_cache()
def get_settings() -> SteamSourceSettings:
    return SteamSourceSettings()  # type: ignore "Load variables from steam_source_variables.env file"


STEAM_SOURCE_SETTINGS = Annotated[SteamSourceSettings, Depends(get_settings)]


async def get_aiohttp_session():
    async with ClientSession() as session:
        yield session


async def get_steam_source_service(
    settings: STEAM_SOURCE_SETTINGS, aiohttp_session: ClientSession = Depends(get_aiohttp_session)
) -> AsyncGenerator[SteamSourceService, Any]:
    async with SteamMarketSourceService(
        settings, aiohttp_session
    ) as steam_market_service, FloatSourceService(settings, aiohttp_session) as float_service:
        steam_source_service = SteamSourceService(
            steam_market_source_service=steam_market_service, float_source_service=float_service
        )
        try:
            yield steam_source_service
        finally:
            await aiohttp_session.close()


STEAM_SOURCE_SERVICE = Annotated[SteamSourceService, Depends(get_steam_source_service)]
