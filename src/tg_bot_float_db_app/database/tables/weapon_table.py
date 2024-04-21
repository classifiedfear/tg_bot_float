import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from tg_bot_float_db_app.database.models import WeaponModel, SkinModel, RelationModel
from tg_bot_float_db_app.database.tables.interface import Table


class WeaponTable(Table):
    async def create(self, model: WeaponModel) -> None:
        await super().create(model)

    async def get_by_id(self, id: int) -> typing.Type[WeaponModel] | None:
        return await self._session.get(WeaponModel, id)

    async def update_by_id(self, id: int, **values) -> typing.Type[WeaponModel] | None:
        update_stmt = sqlalchemy.update(WeaponModel).values(**values)
        where_stmt = update_stmt.where(WeaponModel.id == id)
        returning_stmt = where_stmt.returning(WeaponModel)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_id(self, id: int) -> bool:
        if (weapon := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(weapon)
        await self._session.flush()
        return True

    async def create_many(self, models: typing.List[WeaponModel]) -> None:
        await super().create_many(models)

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        delete_stmt = sqlalchemy.delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(WeaponModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(WeaponModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, item_name: str) -> WeaponModel:
        stmt = sqlalchemy.select(WeaponModel).where(WeaponModel.name == item_name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, weapon_name: str, **values):
        update_stmt = sqlalchemy.update(WeaponModel).values(**values)
        where_stmt = update_stmt.where(WeaponModel.name == weapon_name)
        returning_stmt = where_stmt.returning(WeaponModel)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_name(self, item_name: str) -> bool:
        if (weapon := await self.get_by_name(item_name)) is None:
            return False
        await self._session.delete(weapon)
        await self._session.flush()
        return True

    async def get_all(self) -> sqlalchemy.ScalarResult[WeaponModel]:
        stmt = sqlalchemy.select(WeaponModel)
        return await self._session.scalars(stmt)

    async def get_skins_for_weapon(self, weapon_name: str) -> sqlalchemy.ScalarResult[SkinModel]:
        stmt = (
            sqlalchemy.select(SkinModel)
            .join(SkinModel.w_s_q)
            .join(RelationModel.weapon)
            .where(WeaponModel.name == weapon_name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
