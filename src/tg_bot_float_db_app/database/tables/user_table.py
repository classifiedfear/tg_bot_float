import sqlalchemy
from sqlalchemy import delete
from sqlalchemy.dialects import postgresql

from tg_bot_float_db_app.database.models import User
from tg_bot_float_db_app.database.tables.interface import Table


class UserTable(Table):
    async def create(self, id: int, username: str, full_name: str):
        stmt = postgresql.insert(User).values(id=id, username=username, full_name=full_name)
        await self._session.execute(stmt)

    async def get_by_id(self, id: int) -> User:
        stmt = sqlalchemy.select(User).where(User.id == id)
        return await self._session.scalar(stmt)

    async def delete_by_id(self, id: int) -> None:
        stmt = delete(User).where(User.id == id)
        await self._session.execute(stmt)