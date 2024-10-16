from typing import Awaitable, Callable

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from tg_bot_float_csm_wiki_source.csm_wiki_source_exceptions import CsmWikiSourceExceptions
from tg_bot_float_csm_wiki_source.csm_wiki_constants import NO_INFO_ERROR_MSG


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        try:
            return await call_next(request)
        except CsmWikiSourceExceptions as exc:
            if NO_INFO_ERROR_MSG in exc.message:
                return JSONResponse(status_code=404, content={"message": exc.message})
            return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"message": exc.message},
                )

