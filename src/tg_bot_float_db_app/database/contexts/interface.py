import abc
import typing

from sqlalchemy.ext import asyncio as async_alchemy


class Table:
    def __init__(self, session: async_alchemy.AsyncSession):
        self._session = session

    @abc.abstractmethod
    async def create(self, model):
        self._session.add(model)
        await self._session.flush()

    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def update_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def delete_by_id(self, *args, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    async def create_many(self, models):
        self._session.add_all(models)
        await self._session.flush()

    @abc.abstractmethod
    async def get_many_by_id(self, ids: typing.List[int]):
        pass

    @abc.abstractmethod
    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        pass

    @abc.abstractmethod
    async def get_by_name(self, item_name: str):
        pass

    @abc.abstractmethod
    async def update_by_name(self, item_name: str, **values):
        pass

    @abc.abstractmethod
    async def delete_by_name(self, item_name: str) -> bool:
        pass

    @abc.abstractmethod
    async def get_many_by_name(self, names: typing.List[str]):
        pass

    @abc.abstractmethod
    async def delete_many_by_name(self, item_names: typing.List[str]):
        pass

    @abc.abstractmethod
    async def upsert(self, **values):
        pass

    @abc.abstractmethod
    async def get_all(self):
        pass

    async def save_changes(self):
        await self._session.commit()
