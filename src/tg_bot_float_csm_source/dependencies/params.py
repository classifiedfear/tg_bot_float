from typing import Annotated

from fastapi import Depends

from tg_bot_float_csm_source.routers.csm_params.get_csm_skin_data_params import GetCsmSkinDataParams


GET_CSM_SKIN_DATA_PARAMS = Annotated[GetCsmSkinDataParams, Depends(GetCsmSkinDataParams)]
