from typing import Annotated, AsyncIterable

from fastapi import Depends
from tg_bot_float_csgo_db_source.response_service.csgo_db_response_service import (
    CsgoDbSourceResponseService,
)


async def get_csgo_db_source_response_service() -> AsyncIterable[CsgoDbSourceResponseService]:
    async with CsgoDbSourceResponseService() as service:
        yield service


CSGO_DB_SOURCE_RESPONSE_SERVICE = Annotated[
    CsgoDbSourceResponseService, Depends(get_csgo_db_source_response_service)
]
