from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_wiki_source.services.csm_wiki_source_service import CsmWikiSourceService
from tg_bot_float_csm_wiki_source.csm_wiki_source_settings import CsmWikiSourceSettings


@lru_cache
def get_csm_wiki_source_settings() -> CsmWikiSourceSettings:
    return CsmWikiSourceSettings()


CSM_WIKI_SOURCE_SETTINGS = Annotated[CsmWikiSourceSettings, Depends(get_csm_wiki_source_settings)]


def get_csm_wiki_source_service(settings: CSM_WIKI_SOURCE_SETTINGS) -> CsmWikiSourceService:
    return CsmWikiSourceService(settings)


CSM_WIKI_SKIN_SERVICE = Annotated[CsmWikiSourceService, Depends(get_csm_wiki_source_service)]
