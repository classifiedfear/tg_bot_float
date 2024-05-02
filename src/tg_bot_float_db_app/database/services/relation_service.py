from typing import Tuple, List

import sqlalchemy
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.quality_model import QualityModel

from tg_bot_float_common_dtos.relation_id_dto import RelationIdDTO
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException



class RelationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, relation_id_dto: RelationIdDTO) -> RelationModel:
        relation_model = RelationModel(**relation_id_dto.model_dump(
            exclude_none=True, exclude={"id"}
            ))
        self._session.add(relation_model)
        await self._commit_and_rollback_if_errors()
        return relation_model

    async def create_many(self, relation_dtos: List[RelationIdDTO]) -> List[RelationModel]:
        relation_models = [RelationModel(**relation_dto.model_dump(
            exclude_none=True, exclude={"id"}
            )) for relation_dto in relation_dtos]
        self._session.add_all(relation_models)
        await self._commit_and_rollback_if_errors()
        return relation_models

    async def get_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> RelationModel | None:
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
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def delete_many_by_id(self, ids: List[Tuple[int, int, int]]) -> None:
        delete_stmt = sqlalchemy.delete(RelationModel)
        where_stmt = delete_stmt.where(
            sqlalchemy.tuple_(
                RelationModel.weapon_id,
                RelationModel.skin_id,
                RelationModel.quality_id
            ).in_(ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(ids):
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def get_many_by_id(self, ids: List[Tuple[int, int, int]]):
        select_stmt = sqlalchemy.select(RelationModel)
        where_stmt = select_stmt.where(
            sqlalchemy.tuple_(
                RelationModel.weapon_id,
                RelationModel.skin_id,
                RelationModel.quality_id
            ).in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_qualities_for_weapon_and_skin(self, weapon_id: int, skin_id: int):
        stmt = (
            sqlalchemy.select(QualityModel)
            .join(QualityModel.relations)
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
            .join(SkinModel.relations)
            .join(RelationModel.weapon)
            .join(RelationModel.quality)
            .order_by(sqlalchemy.func.random)
            .limit(1)
        )
        return await self._session.scalar(stmt)

    async def _commit_and_rollback_if_errors(self) -> None:
        try:
            await self._session.commit()
        except:
            await self._session.rollback()
            raise

