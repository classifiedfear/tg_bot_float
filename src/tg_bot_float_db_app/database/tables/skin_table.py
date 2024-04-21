import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from tg_bot_float_db_app.database.models import SkinModel
from tg_bot_float_db_app.database.tables.interface import Table


class SkinTable(Table):

    async def create(self, model: SkinModel) -> None:
        await super().create(model)

    async def get_by_id(self, id: int) -> typing.Type[SkinModel] | None:
        return await self._session.get(SkinModel, id)

    async def update_by_id(self, id: int, **values) -> typing.Type[SkinModel] | None:
        update_stmt = sqlalchemy.update(SkinModel).values(**values)
        where_stmt = update_stmt.where(SkinModel.id == id)
        returning_stmt = where_stmt.returning(SkinModel)
        skin = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return skin

    async def delete_by_id(self, id: int) -> bool:
        if (skin := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(skin)
        await self._session.flush()
        return True

    async def create_many(self, models: typing.List[SkinModel]) -> None:
        await super().create_many(models)

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]):
        delete_stmt = sqlalchemy.delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(SkinModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(SkinModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> typing.Type[SkinModel] | None:
        stmt = sqlalchemy.select(SkinModel).where(SkinModel.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, name: str, **values) -> typing.Type[SkinModel] | None:
        update_stmt = sqlalchemy.update(SkinModel).values(**values)
        where_stmt = update_stmt.where(SkinModel.name == name)
        returning_stmt = where_stmt.returning(SkinModel)
        skin = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return skin

    async def delete_by_name(self, skin_name: str) -> bool:
        if (skin := await self.get_by_name(skin_name)) is None:
            return False
        await self._session.delete(skin)
        await self._session.flush()
        return True

    async def get_all(self) -> sqlalchemy.ScalarResult[SkinModel]:
        stmt = sqlalchemy.select(SkinModel)
        return await self._session.scalars(stmt)

    async def get_stattrak_existence_for_skin(self, skin_name: str) -> bool:
        stmt = sqlalchemy.select(SkinModel.stattrak_existence).where(
            SkinModel.name == skin_name)
        return await self._session.scalar(stmt)

