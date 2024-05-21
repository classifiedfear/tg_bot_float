from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_source.services.csm_source_service import CsmService

CSM_SERVICE = Annotated[CsmService, Depends(CsmService)]
