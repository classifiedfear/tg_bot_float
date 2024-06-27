from typing import Awaitable, Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from tg_bot_float_steam_source.services.steam_source_exceptions import (
    IncorrectDataException,
    TooManyRequestsException,
)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except IncorrectDataException as exc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.msg}
            )
        except TooManyRequestsException as exc:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"message": exc.msg}
            )
