from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_source.router_controllers.csm_router_params.csm_params import CsmParams


CSM_PARAMS = Annotated[CsmParams, Depends(CsmParams)]
