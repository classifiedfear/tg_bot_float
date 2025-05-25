from http import HTTPStatus
from typing import Any, Dict
from aiohttp import ClientSession

from tg_bot_float_telegram_app.tg_settings import TgSettings


class BaseServiceClient:
    _success_responses = list(range(200, 300))

    def __init__(self, settings: TgSettings) -> None:
        self._settings = settings
        self._session = ClientSession()

    async def close(self) -> None:
        await self._session.close()

    async def _get_json_response(self, link: str) -> Any:
        async with self._session.get(link) as response:
            return await response.json()

    async def _delete_request(self, link: str) -> None:
        async with self._session.delete(link) as response:
            assert response.status == HTTPStatus.NO_CONTENT

    async def _post_request(self, link: str, json: Dict[str, Any]) -> None:
        async with self._session.post(link, json=json) as response:
            assert response.status == HTTPStatus.CREATED
