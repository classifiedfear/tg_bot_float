from typing import Annotated

from fastapi import Depends

from tg_bot_float_steam_source.services.steam_sorce_service import SteamSourceService

STEAM_SOURCE_SERVICE = Annotated[SteamSourceService, Depends(SteamSourceService)]
