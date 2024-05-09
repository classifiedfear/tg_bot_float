from http import HTTPStatus
from typing import Tuple, List

from sqlalchemy import select, delete, tuple_, ScalarResult, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.misc.exceptions import BotDbException
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
)
from tg_bot_float_common_dtos.relation_id_dto import RelationIdDTO


class RelationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, relation_id_dto: RelationIdDTO) -> RelationModel:
        relation_model = RelationModel(**relation_id_dto.model_dump(exclude_none=True))
        self._session.add(relation_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=f"{relation_id_dto.weapon_id}, {relation_id_dto.skin_id}, {relation_id_dto.quality_id}",
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
        return relation_model

    async def create_many(self, relation_dtos: List[RelationIdDTO]) -> List[RelationModel]:
        relation_models = [
            RelationModel(**relation_dto.model_dump(exclude_none=True))
            for relation_dto in relation_dtos
        ]
        self._session.add_all(relation_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            existence_relation_db_models = await self.get_many_by_id(
                [
                    (relation_dto.weapon_id, relation_dto.skin_id, relation_dto.quality_id)
                    for relation_dto in relation_dtos
                ]
            )
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Relations",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=", ".join(
                        f"({relation.weapon_id}, {relation.skin_id}, {relation.quality_id})"
                        for relation in existence_relation_db_models
                    ),
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
        return relation_models

    async def get_by_id(
        self, weapon_id: int, skin_id: int, quality_id: int
    ) -> RelationModel | None:
        relation_model = await self._session.get(
            RelationModel, {"weapon_id": weapon_id, "skin_id": skin_id, "quality_id": quality_id}
        )
        if relation_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=f"{weapon_id}, {skin_id}, {quality_id}",
                ),
                HTTPStatus.NOT_FOUND,
            )
        return relation_model

    async def get_all(self) -> ScalarResult[RelationModel]:
        select_stmt = select(RelationModel)
        return await self._session.scalars(select_stmt)

    async def delete_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        del_stmt = delete(RelationModel)
        where_stmt = del_stmt.where(
            RelationModel.weapon_id == weapon_id,
            RelationModel.skin_id == skin_id,
            RelationModel.quality_id == quality_id,
        )
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=f"{weapon_id}, {skin_id}, {quality_id}",
                ),
                HTTPStatus.NOT_FOUND,
            )
        await self._session.commit()

    async def delete_many_by_id(self, ids: List[Tuple[int, int, int]]) -> None:
        delete_stmt = delete(RelationModel)
        where_stmt = delete_stmt.where(
            tuple_(RelationModel.weapon_id, RelationModel.skin_id, RelationModel.quality_id).in_(
                ids
            )
        )
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(ids):
            existence_relation_db_models = await self.get_many_by_id(ids)
            existence_ids = {
                (relation.weapon_id, relation.skin_id, relation.quality_id)
                for relation in existence_relation_db_models
            }
            difference_ids = set(ids).symmetric_difference(existence_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=", ".join(f"{ids}" for ids in difference_ids),
                ),
                HTTPStatus.NOT_FOUND,
            )
        await self._session.commit()

    async def get_many_by_id(self, ids: List[Tuple[int, int, int]]):
        select_stmt = select(RelationModel)
        where_stmt = select_stmt.where(
            tuple_(RelationModel.weapon_id, RelationModel.skin_id, RelationModel.quality_id).in_(
                ids
            )
        )
        return await self._session.scalars(where_stmt)

    async def get_qualities_for_weapon_and_skin(self, weapon_id: int, skin_id: int):
        stmt = (
            select(QualityModel)
            .join(QualityModel.relations)
            .join(RelationModel.weapon)
            .join(RelationModel.skin)
            .where(WeaponModel.id == weapon_id, SkinModel.id == skin_id)
        )
        return await self._session.scalars(stmt)

    async def get_random_weapon_from_db(self):
        stmt = (
            select(
                SkinModel.name, WeaponModel.name, QualityModel.name, SkinModel.stattrak_existence
            )
            .join(SkinModel.relations)
            .join(RelationModel.weapon)
            .join(RelationModel.quality)
            .order_by(func.random)
            .limit(1)
        )
        return await self._session.scalar(stmt)

    async def get_skins_by_name_for(
        self,
        weapon_name: str | None = None,
        quality_name: str | None = None,
        stattrak_existence: bool | None = None,
    ):
        stmt = select(SkinModel).join(SkinModel.relations)
        if weapon_name is not None:
            stmt = stmt.join(RelationModel.weapon).where(WeaponModel.name == weapon_name)
        if quality_name is not None:
            stmt = stmt.join(RelationModel.quality).where(QualityModel.name == quality_name)
        if stattrak_existence is not None:
            stmt = stmt.where(SkinModel.stattrak_existence == stattrak_existence)
        return await self._session.scalars(stmt.distinct())

    async def get_skins_by_id_for(
        self,
        weapon_id: int | None = None,
        quality_id: int | None = None,
        stattrak_existence: bool | None = None,
    ):
        stmt = select(SkinModel).join(SkinModel.relations)
        if weapon_id is not None:
            stmt = stmt.join(RelationModel.weapon).where(WeaponModel.id == weapon_id)
        if quality_id is not None:
            stmt = stmt.join(RelationModel.quality).where(QualityModel.id == quality_id)
        if stattrak_existence is not None:
            stmt = stmt.where(SkinModel.stattrak_existence == stattrak_existence)
        return await self._session.scalars(stmt.distinct())
