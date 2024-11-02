from typing import Annotated

from fastapi import Depends

from tg_bot_float_steam_source.router_controllers.steam_router_params.steam_params import SteamParams


STEAM_PARAMS = Annotated[SteamParams, Depends(SteamParams)]
