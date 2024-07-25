from functools import lru_cache
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends

from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.weapon_page_service import WeaponPageService
from tg_bot_float_csgo_db_source.services.skin_page_service import SkinPageService


@lru_cache
def get_settings():
    return CsgoDbSourceSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"


CSGO_DB_SOURCE_SETTINGS = Annotated[CsgoDbSourceSettings, Depends(get_settings)]


async def get_weapon_page_service(
    settings: CSGO_DB_SOURCE_SETTINGS,
) -> WeaponPageService:
    # async with WeaponPageService(settings) as weapon_page_service:
    #    yield weapon_page_service
    return WeaponPageService(settings)


async def get_skin_page_service(
    settings: CSGO_DB_SOURCE_SETTINGS,
) -> SkinPageService:
    # async with SkinPageService(settings) as skin_page_service:
    #    yield skin_page_service
    return SkinPageService(settings)


WEAPON_PAGE_SERVICE = Annotated[WeaponPageService, Depends(get_weapon_page_service)]

SKIN_PAGE_SERVICE = Annotated[SkinPageService, Depends(get_skin_page_service)]
