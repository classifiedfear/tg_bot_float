from typing import Annotated

from fastapi import Depends

from tg_bot_float_steam_source.routers.steam_params.get_steam_skin_data_params import (
    GetSteamSkinDataParams,
)


GET_STEAM_SKIN_DATA_PARAMS = Annotated[GetSteamSkinDataParams, Depends(GetSteamSkinDataParams)]
