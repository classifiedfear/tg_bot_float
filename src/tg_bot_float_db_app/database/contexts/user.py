import sqlalchemy
from sqlalchemy import delete
from sqlalchemy.dialects import postgresql

from tg_bot_float_db_app.database.models.user_models import UserModel
from tg_bot_float_db_app.database.contexts.interface import Table


class UserContext(Table):
    async def create(self, id: int, username: str, full_name: str):
        stmt = postgresql.insert(UserModel).values(id=id, username=username, full_name=full_name)
        await self._session.execute(stmt)

    async def get_by_id(self, id: int) -> UserModel:
        stmt = sqlalchemy.select(UserModel).where(UserModel.id == id)
        return await self._session.scalar(stmt)

    async def delete_by_id(self, id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == id)
        await self._session.execute(stmt)