from typing import Awaitable, Callable

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        try:
            return await call_next(request)
        except CsgoDbException as exc:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": exc.message},
            )
