from functools import lru_cache
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends

from tg_bot_float_csm_source.csm_source_settings import CsmSourceSettings
from tg_bot_float_csm_source.services.csm_source_service import CsmService


@lru_cache
def get_settings() -> CsmSourceSettings:
    return CsmSourceSettings() #type: ignore "Load variables from csm_source_variables.env file"


CSM_SOURCE_SETTINGS = Annotated[CsmSourceSettings, Depends(get_settings)]


async def get_csm_service(settings: CSM_SOURCE_SETTINGS) -> AsyncGenerator[Any, CsmService]:
    async with CsmService(settings) as service:
        yield service


CSM_SERVICE = Annotated[CsmService, Depends(get_csm_service)]
