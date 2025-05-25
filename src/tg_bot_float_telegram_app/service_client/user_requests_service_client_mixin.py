from typing import Any, Dict

from tg_bot_float_common_dtos.schema_dtos.user_dto import UserDTO
from tg_bot_float_telegram_app.service_client.base_service_client import BaseServiceClient


class UserRequestsServiceClientMixin(BaseServiceClient):

    async def create_user(self, telegram_id: int, username: str, full_name: str) -> int:
        create_user_url = self._settings.db_app_base_url + self._settings.create_user_url
        user: Dict[str, Any] = {
            "telegram_id": telegram_id,
            "username": username,
            "full_name": full_name,
        }
        async with self._session.post(create_user_url, json=user) as response:
            if response.status in self._success_responses:
                location_header: str = response.headers["Location"]
                user_id = location_header.removeprefix("/users/id/")
                return int(user_id)
            raise AssertionError("User creation failed, response status: {response.status}")

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO | None:
        get_user_url = self._settings.db_app_base_url + self._settings.get_user_url.format(
            telegram_id=telegram_id
        )
        response_json = await self._get_json_response(get_user_url)
        if not response_json.get("message"):
            return UserDTO.model_validate(response_json)

    async def delete_user_by_telegram_id(self, telegram_id: int) -> None:
        delete_user_url = self._settings.db_app_base_url + self._settings.delete_user_url.format(
            telegram_id=telegram_id
        )
        await self._delete_request(delete_user_url)

    async def get_users_telegram_ids_by_subscription(self):
        pass
