from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_source.csm_source_settings import CsmSourceSettings
from tg_bot_float_csm_source.services.csm_source_service import CsmService


@lru_cache
def get_settings() -> CsmSourceSettings:
    return CsmSourceSettings()


CSM_SOURCE_SETTINGS = Annotated[CsmSourceSettings, Depends(get_settings)]


def get_csm_service(settings: CSM_SOURCE_SETTINGS) -> CsmService:
    return CsmService(settings)


CSM_SERVICE = Annotated[CsmService, Depends(get_csm_service)]
