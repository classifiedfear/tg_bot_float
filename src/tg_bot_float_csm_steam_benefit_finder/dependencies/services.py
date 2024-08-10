from functools import lru_cache
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from tg_bot_float_csm_steam_benefit_finder.csm_steam_benefit_finder_settings import (
    CsmSteamBenefitFinderSettings,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.csm_steam_benefit_finder_service import (
    CsmSteamBenefitFinderService,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.source_data_getter_service import (
    SourceDataGetterService,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.csm_steam_benefit_sender_service import (
    CsmSteamBenefitSenderService,
)


@lru_cache
def get_benefit_finder_settings() -> CsmSteamBenefitFinderSettings:
    return CsmSteamBenefitFinderSettings()  # type: ignore "Load variables from csm_steam_benefit_finder_variables.env"


CSM_STEAM_BENEFIT_FINDER_SETTINGS = Annotated[
    CsmSteamBenefitFinderSettings, Depends(get_benefit_finder_settings)
]


async def get_aiohttp_session():
    async with ClientSession() as session:
        yield session


async def get_benefit_finder_service(
    settings: CSM_STEAM_BENEFIT_FINDER_SETTINGS,
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    async with SourceDataGetterService(
        settings, aiohttp_session
    ) as getter_service, CsmSteamBenefitSenderService(settings, aiohttp_session) as sender_service:
        try:
            yield CsmSteamBenefitFinderService(getter_service, sender_service)
        finally:
            await aiohttp_session.close()


CSM_STEAM_BENEFIT_FINDER_SERVICE = Annotated[
    CsmSteamBenefitFinderService, Depends(get_benefit_finder_service)
]
