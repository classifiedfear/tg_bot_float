import typing
from typing import Type

import sqlalchemy
from sqlalchemy import ScalarResult
from sqlalchemy.dialects import postgresql

from tg_bot_float_db_app.database.models.skin_models import SkinModel, RelationModel, WeaponModel, QualityModel
from tg_bot_float_db_app.database.contexts.interface import Table


class RelationsContext(Table):
    async def create(self, model: RelationModel) -> None:
        await super().create(model)

    async def create_many(self, models: typing.List[RelationModel]) -> None:
        await super().create_many(models)

    async def get_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> Type[RelationModel] | None:
        return await self._session.get(RelationModel, {
            "weapon_id": weapon_id,
            "skin_id": skin_id,
            "quality_id": quality_id
        })

    async def get_all(self) -> ScalarResult[RelationModel]:
        select_stmt = sqlalchemy.select(RelationModel)
        return await self._session.scalars(select_stmt)

    async def delete_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        del_stmt = sqlalchemy.delete(RelationModel)
        where_stmt = del_stmt.where(
            RelationModel.weapon_id == weapon_id,
            RelationModel.skin_id == skin_id,
            RelationModel.quality_id == quality_id
        )
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_id(self, ids: typing.List[typing.Tuple[int, int, int]]) -> None:
        delete_stmt = sqlalchemy.delete(RelationModel)
        where_stmt = delete_stmt.where(
            sqlalchemy.tuple_(
                RelationModel.weapon_id,
                RelationModel.skin_id,
                RelationModel.quality_id
            ).in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def update_by_id(self, weapon_id: int, skin_id: int, quality_id: int, **values):
        relation = await self.get_by_id(weapon_id, skin_id, quality_id)
        relation.weapon_id = id if (id := values.get('weapon_id')) else relation.weapon_id
        relation.skin_id = id if (id := values.get('skin_id')) else relation.skin_id
        relation.quality_id = id if (id := values.get('quality_id')) else relation.quality_id
        await self._session.flush()
        return relation

    async def upsert(self, **values):
        stmt = postgresql.insert(RelationModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(RelationModel)
        return await self._session.scalar(returning_stmt)

    async def get_qualities_for_weapon_and_skin(self, weapon_id: int, skin_id: int):
        stmt = (
            sqlalchemy.select(QualityModel)
            .join(QualityModel.w_s_q)
            .join(RelationModel.weapon)
            .join(RelationModel.skin)
            .where(WeaponModel.id == weapon_id, SkinModel.id == skin_id)
        )
        return await self._session.scalars(stmt)

    async def get_random_weapon_from_db(self):
        stmt = (
            sqlalchemy.select(
                SkinModel.name,
                WeaponModel.name,
                QualityModel.name,
                SkinModel.stattrak_existence
            )
            .join(SkinModel.w_s_q)
            .join(RelationModel.weapon)
            .join(RelationModel.quality)
            .order_by(sqlalchemy.func.random)
            .limit(1)
        )
        return await self._session.scalar(stmt)

