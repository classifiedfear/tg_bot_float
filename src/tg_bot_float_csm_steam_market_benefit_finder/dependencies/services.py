from functools import lru_cache
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from tg_bot_float_csm_steam_market_benefit_finder.csm_steam_market_benefit_finder_settings import (
    CsmSteamMarketBenefitFinderSettings,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.csm_steam_market_benefit_finder_service import (
    CsmSteamMarketBenefitFinderService,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.subscription_source_data_getter import (
    SubscriptionSourceDataGetter,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.csm_steam_source_data_getter import (
    CsmSteamMarketSourceDataGetter,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.result_sender_service import (
    ResultSenderService,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.csm_steam_comparer import (
    CsmSteamComparer,
)


@lru_cache
def get_benefit_finder_settings() -> CsmSteamMarketBenefitFinderSettings:
    return CsmSteamMarketBenefitFinderSettings()  # type: ignore "Load variables from csm_steam_benefit_finder_variables.env"


CSM_STEAM_BENEFIT_FINDER_SETTINGS = Annotated[
    CsmSteamMarketBenefitFinderSettings, Depends(get_benefit_finder_settings)
]


async def get_aiohttp_session():
    async with ClientSession() as session:
        yield session


async def get_csm_steam_market_benefit_finder_service(
    settings: CSM_STEAM_BENEFIT_FINDER_SETTINGS,
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    async with CsmSteamMarketSourceDataGetter(
        settings, aiohttp_session
    ) as csm_steam_source_getter, SubscriptionSourceDataGetter(
        settings, aiohttp_session
    ) as subscription_source_getter, ResultSenderService(
        settings, aiohttp_session
    ) as sender_service:
        comparer = CsmSteamComparer()
        try:
            yield CsmSteamMarketBenefitFinderService(
                csm_steam_source_data_getter=csm_steam_source_getter,
                subscription_source_data_getter=subscription_source_getter,
                csm_steam_comparer=comparer,
                result_sender_service=sender_service,
            )
        finally:
            await aiohttp_session.close()


CSM_STEAM_MARKET_BENEFIT_FINDER_SERVICE = Annotated[
    CsmSteamMarketBenefitFinderService, Depends(get_csm_steam_market_benefit_finder_service)
]
