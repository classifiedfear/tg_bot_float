from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_wiki_source.services.csm_wiki_source_service import CsmWikiSurceService

CSM_WIKI_SKIN_SERVICE = Annotated[CsmWikiSurceService, Depends(CsmWikiSurceService)]
