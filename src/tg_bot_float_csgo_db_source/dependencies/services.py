from typing import Annotated
from functools import lru_cache

from fastapi import Depends

from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.agents_page_service import AgentsPageService
from tg_bot_float_csgo_db_source.services.gloves_page_service import GlovesPageService
from tg_bot_float_csgo_db_source.services.weapons_page_service import WeaponsPageService
from tg_bot_float_csgo_db_source.services.skins_page_service import SkinsPageService


@lru_cache
def get_settings():
    return CsgoDbSourceSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"


CSGO_DB_SOURCE_SETTINGS = Annotated[CsgoDbSourceSettings, Depends(get_settings)]


async def get_weapon_page_service(settings: CSGO_DB_SOURCE_SETTINGS) -> WeaponsPageService:
    return WeaponsPageService(settings)


async def get_skin_page_service(settings: CSGO_DB_SOURCE_SETTINGS) -> SkinsPageService:
    return SkinsPageService(settings)


async def get_glove_page_service(settings: CSGO_DB_SOURCE_SETTINGS) -> GlovesPageService:
    return GlovesPageService(settings)


async def get_agent_page_service(settings: CSGO_DB_SOURCE_SETTINGS) -> AgentsPageService:
    return AgentsPageService(settings)


WEAPON_PAGE_SERVICE = Annotated[WeaponsPageService, Depends(get_weapon_page_service)]

SKIN_PAGE_SERVICE = Annotated[SkinsPageService, Depends(get_skin_page_service)]

GLOVE_PAGE_SERVICE = Annotated[GlovesPageService, Depends(get_glove_page_service)]

AGENT_PAGE_SERVICE = Annotated[AgentsPageService, Depends(get_agent_page_service)]
