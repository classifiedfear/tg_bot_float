from sqlalchemy.ext import asyncio as async_alchemy

from tg_bot_float_db_app.database.models.base import Base


class BotDbCreator:
    def __init__(self, engine: async_alchemy.AsyncEngine):
        self._engine = engine

    async def create_all_tables(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)