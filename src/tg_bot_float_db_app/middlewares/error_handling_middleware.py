from typing import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from tg_bot_float_db_app.misc.exceptions import BotDbException


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        try:
            return await call_next(request)
        except BotDbException as exc:
            return JSONResponse(status_code=exc.status,content={"message": exc.msg})
