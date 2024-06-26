from typing import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from tg_bot_float_csm_source.services.exceptions import CsmSourceExceptions


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except CsmSourceExceptions as exc:
            return JSONResponse(content={"message": exc.msg})
