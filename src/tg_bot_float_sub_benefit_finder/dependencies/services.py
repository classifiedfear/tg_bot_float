from functools import lru_cache
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from tg_bot_float_sub_benefit_finder.sub_benefit_finder_settings import (
    CsmSteamBenefitFinderSettings,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.sub_benefit_finder_service import (
    SubBenefitFinderService,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.source_data_getter_service import (
    SourceDataGetterService,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.result_sender_service import (
    ResultSenderService,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.csm_steam_comparer import (
    CsmSteamComparer,
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
    ) as getter_service, ResultSenderService(settings, aiohttp_session) as sender_service:
        comparer = CsmSteamComparer()
        try:
            yield SubBenefitFinderService(getter_service, sender_service, comparer)
        finally:
            await aiohttp_session.close()


CSM_STEAM_BENEFIT_FINDER_SERVICE = Annotated[
    SubBenefitFinderService, Depends(get_benefit_finder_service)
]
