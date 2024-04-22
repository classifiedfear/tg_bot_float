import typing
from typing import Type

import sqlalchemy

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.skin_models import QualityModel


class QualityContext:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, model: QualityModel) -> None:
        self._session.add(model)
        await self._session.flush()

    async def get_by_id(self, id: int) -> Type[QualityModel] | None:
        return await self._session.get(QualityModel, id)

    async def update_by_id(self, id: int, **values):
        update_stmt = sqlalchemy.update(QualityModel).values(**values)
        where_stmt = update_stmt.where(QualityModel.id == id)
        returning_stmt = where_stmt.returning(QualityModel)
        quality = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return quality

    async def delete_by_id(self, id: int) -> bool:
        if (quality := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(quality)
        await self._session.flush()
        return True

    async def create_many(self, models: typing.List[QualityModel]) -> None:
        self._session.add_all(models)
        await self._session.flush()

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        delete_stmt = sqlalchemy.delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(QualityModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(QualityModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> Type[QualityModel] | None:
        stmt = sqlalchemy.select(QualityModel).where(QualityModel.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, quality_name: str, **values):
        update_stmt = sqlalchemy.update(QualityModel).values(**values)
        where_stmt = update_stmt.where(QualityModel.name == quality_name)
        returning_stmt = where_stmt.returning(QualityModel)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_name(self, quality_name: str) -> bool:
        if (quality_model := await self.get_by_name(quality_name)) is None:
            return False
        await self._session.delete(quality_model)
        await self._session.flush()
        return True


    async def get_all(self) -> sqlalchemy.ScalarResult[QualityModel]:
        stmt = sqlalchemy.select(QualityModel)
        return await self._session.scalars(stmt)

    async def save_changes(self) -> None:
        await self._session.commit()


