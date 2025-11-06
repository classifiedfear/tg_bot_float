from http import HTTPStatus

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.models import Response
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_misc.response_service.abstract_response_service import AbstractResponseService


class CsgoDbSourceResponseService(AbstractResponseService):
    async def _get_response(self, url: str, session: AsyncSession) -> Response:
        response = await super()._get_response(url, session)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise CsgoDbException("Item with this name not found!")
        return response
