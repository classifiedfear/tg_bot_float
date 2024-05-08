from typing import List
import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO


class WeaponService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, weapon_dto: WeaponDTO) -> WeaponModel:
        weapon_model = WeaponModel(**weapon_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(weapon_model)
        await self._commit_and_rollback_if_errors()
        return weapon_model

    async def get_by_id(self, weapon_id: int) -> WeaponModel | None:
        return await self._session.get(WeaponModel, weapon_id)

    async def update_by_id(self, weapon_id: int, weapon_dto: WeaponDTO) -> WeaponModel | None:
        update_stmt = sqlalchemy.update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.id == weapon_id)
        returning_stmt = where_stmt.returning(WeaponModel)
        weapon_model = await self._session.scalar(returning_stmt)
        if weapon_model is not None:
            await self._commit_and_rollback_if_errors()
        return weapon_model

    async def delete_by_id(self, weapon_id: int) -> None:
        delete_stmt = sqlalchemy.delete(WeaponModel).where(WeaponModel.id == weapon_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def create_many(self, weapon_dtos: List[WeaponDTO]) -> List[WeaponModel]:
        weapon_models = [
            WeaponModel(**weapon_dto.model_dump(exclude_none=True, exclude={"id"}))
            for weapon_dto in weapon_dtos
        ]
        self._session.add_all(weapon_models)
        await self._commit_and_rollback_if_errors()
        return weapon_models

    async def get_many_by_id(self, ids: List[int]):
        select_stmt = sqlalchemy.select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: List[str]):
        select_stmt = sqlalchemy.select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: List[int]) -> None:
        delete_stmt = sqlalchemy.delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.id.in_(ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(ids):
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def delete_many_by_name(self, weapon_names: List[str]):
        delete_stmt = sqlalchemy.delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.name.in_(weapon_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(weapon_names):
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def upsert(self, weapon_dto: WeaponDTO) -> WeaponDTO | None:
        values = weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = postgresql.insert(WeaponModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(WeaponModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, item_name: str) -> WeaponModel | None:
        stmt = sqlalchemy.select(WeaponModel).where(WeaponModel.name == item_name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, weapon_name: str, weapon_dto: WeaponDTO):
        update_stmt = sqlalchemy.update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.name == weapon_name)
        returning_stmt = where_stmt.returning(WeaponModel)
        weapon = await self._session.scalar(returning_stmt)
        await self._commit_and_rollback_if_errors()
        return weapon

    async def delete_by_name(self, weapon_name: str) -> None:
        delete_stmt = sqlalchemy.delete(WeaponModel).where(WeaponModel.name == weapon_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def get_all(self) -> sqlalchemy.ScalarResult[WeaponModel]:
        stmt = sqlalchemy.select(WeaponModel)
        return await self._session.scalars(stmt)

    async def get_skins_for_weapon(self, weapon_name: str) -> sqlalchemy.ScalarResult[SkinModel]:
        stmt = (
            sqlalchemy.select(SkinModel)
            .join(SkinModel.relations)
            .join(RelationModel.weapon)
            .where(WeaponModel.name == weapon_name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)

    async def _commit_and_rollback_if_errors(self) -> None:
        try:
            await self._session.commit()
        except:
            await self._session.rollback()
            raise
