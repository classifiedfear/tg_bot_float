from sqlalchemy.ext import asyncio as async_alchemy

from tg_bot_float_db_app.database.declar_base import Base


class BotDatabaseEngine:
    def __init__(self, url: str):
        self._ulr = url
        self._engine = async_alchemy.create_async_engine(url, echo=True, pool_pre_ping=True)

    async def proceed_schemas(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

    @property
    def engine(self) -> async_alchemy.AsyncEngine:
        return self._engine
