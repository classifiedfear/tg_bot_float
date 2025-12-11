import abc

from typing import Self

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.models import Response


class AbstractResponseService(abc.ABC):
    def __init__(self) -> None:
        self._session = None

    async def __aenter__(self) -> Self:
        self._session = AsyncSession(impersonate="chrome124")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        if self._session:
            await self._session.close()

    async def get_page_html(self, url: str) -> str:
        if not self._session:
            async with AsyncSession(impersonate="chrome124") as session:
                response = await self._get_response(url, session)
                return response.text
        response = await self._get_response(url, self._session)
        return response.text

    async def _get_response(self, url: str, session: AsyncSession) -> Response:
        return await session.get(url)
