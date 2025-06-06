from typing import List

from sqlalchemy import select, delete, tuple_, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)
from tg_bot_float_common_dtos.schema_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.db_app_dtos.relation_name_dto import RelationNameDTO


class RelationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, relation_id_dto: RelationDTO) -> RelationModel:
        relation_model = RelationModel(**relation_id_dto.model_dump(exclude_none=True))
        self._session.add(relation_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(
                exc,
                "weapon_id, skin_id, quality_id, stattrak_existence",
                (
                    f"{relation_id_dto.weapon_id}, "
                    f"{relation_id_dto.skin_id}, "
                    f"{relation_id_dto.quality_id}, "
                    f"{relation_id_dto.stattrak_existence}"
                ),
            )

        return relation_model

    async def create_many(self, relation_dtos: List[RelationDTO]) -> List[RelationModel]:
        relation_models = [
            RelationModel(**relation_dto.model_dump(exclude_none=True))
            for relation_dto in relation_dtos
        ]
        self._session.add_all(relation_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            existence_relation_db_models = await self.get_many_by_id(relation_dtos)
            self._raise_bot_db_exception(
                exc,
                "weapon_id, skin_id, quality_id, stattrak_existence",
                ", ".join(
                    f"({relation.weapon_id}, {relation.skin_id}, {relation.quality_id}, {relation.stattrak_existence})"
                    for relation in existence_relation_db_models
                ),
            )

        return relation_models

    async def get_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> RelationModel:
        select_stmt = select(RelationModel)
        where_stmt = select_stmt.where(
            RelationModel.weapon_id == weapon_id,
            RelationModel.skin_id == skin_id,
            RelationModel.quality_id == quality_id,
        )
        relation_model = await self._session.scalar(where_stmt)
        if relation_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id",
                    entity_identifier=f"{weapon_id}, {skin_id}, {quality_id}",
                ),
            )
        return relation_model

    async def get_all(self) -> ScalarResult[RelationModel]:
        select_stmt = select(RelationModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[RelationModel]:
        select_stmt = select(RelationModel)
        return await paginate(self._session, select_stmt)

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
            )
        await self._session.commit()

    async def delete_many_by_id(self, relation_id_dtos: List[RelationDTO]) -> None:
        relation_id_tuple = [
            (
                relation_id.weapon_id,
                relation_id.skin_id,
                relation_id.quality_id,
                relation_id.stattrak_existence,
            )
            for relation_id in relation_id_dtos
        ]
        stmt = delete(RelationModel).where(
            tuple_(
                RelationModel.weapon_id,
                RelationModel.skin_id,
                RelationModel.quality_id,
                RelationModel.stattrak_existence,
            ).in_(relation_id_tuple)
        )
        result = await self._session.execute(stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(relation_id_dtos):
            await self._session.rollback()
            existence_relation_db_models = await self.get_many_by_id(relation_id_dtos)
            existence_ids = {
                (
                    relation.weapon_id,
                    relation.skin_id,
                    relation.quality_id,
                    relation.stattrak_existence,
                )
                for relation in existence_relation_db_models
            }
            difference_ids = set(relation_id_tuple).symmetric_difference(existence_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier="weapon_id, skin_id, quality_id, stattrak_existence",
                    entity_identifier=", ".join(f"{ids}" for ids in difference_ids),
                ),
            )
        await self._session.commit()

    async def get_many_by_id(self, relation_id_dtos: List[RelationDTO]):
        relation_id_tuple = [
            (
                relation_id.weapon_id,
                relation_id.skin_id,
                relation_id.quality_id,
                relation_id.stattrak_existence,
            )
            for relation_id in relation_id_dtos
        ]
        select_stmt = select(RelationModel)
        where_stmt = select_stmt.where(
            tuple_(
                RelationModel.weapon_id,
                RelationModel.skin_id,
                RelationModel.quality_id,
                RelationModel.stattrak_existence,
            ).in_(relation_id_tuple)
        )
        return await self._session.scalars(where_stmt)

    async def get_weapon_skin_quality_name_by_id(
        self, weapon_id: int, skin_id: int, quality_id: int
    ) -> RelationNameDTO:
        select_stmt = (
            select(
                WeaponModel.name,
                SkinModel.name,
                QualityModel.name,
                RelationModel.stattrak_existence,
            )
            .join(WeaponModel.relations)
            .join(RelationModel.skin)
            .join(RelationModel.quality)
        )
        where_stmt = select_stmt.where(
            WeaponModel.id == weapon_id,
            SkinModel.id == skin_id,
            QualityModel.id == quality_id,
        )
        result = await self._session.execute(where_stmt)
        row = result.one_or_none()
        if row is not None:
            weapon_name, skin_name, quality_name, stattrak_existence = row.tuple()
            return RelationNameDTO(
                weapon_name=weapon_name,
                skin_name=skin_name,
                quality_name=quality_name,
                stattrak_existence=stattrak_existence,
            )
        raise BotDbException(
            ENTITY_NOT_FOUND_ERROR_MSG.format(
                entity="Relation",
                identifier="weapon_id, skin_id, quality_id",
                entity_identifier=f"{weapon_id}, {skin_id}, {quality_id}",
            ),
        )

    async def get_stattrak_existence(self, weapon_id: int, skin_id: int, quality_id: int) -> bool:
        select_stmt = select(RelationModel.stattrak_existence)
        where_stmt = select_stmt.where(
            RelationModel.weapon_id == weapon_id,
            RelationModel.skin_id == skin_id,
            RelationModel.quality_id == quality_id,
        )
        result = await self._session.scalar(where_stmt)
        if result is not None:
            return result
        raise BotDbException(
            ENTITY_NOT_FOUND_ERROR_MSG.format(
                entity="Relation",
                identifier="weapon_id, skin_id, quality_id",
                entity_identifier=f"{weapon_id}, {skin_id}, {quality_id}",
            ),
        )

    async def get_weapon_skin_quality_id_by_name(
        self, weapon_name: str, skin_name: str, quality_name: str
    ) -> RelationDTO:
        select_stmt = (
            select(WeaponModel.id, SkinModel.id, QualityModel.id, RelationModel.stattrak_existence)
            .join(WeaponModel.relations)
            .join(RelationModel.skin)
            .join(RelationModel.quality)
        )
        where_stmt = select_stmt.where(
            WeaponModel.name == weapon_name,
            SkinModel.name == skin_name,
            QualityModel.name == quality_name,
        )
        result = await self._session.execute(where_stmt)
        row = result.one_or_none()
        if row is not None:
            weapon_id, skin_id, quality_id, stattrak_existence = row.tuple()
            return RelationDTO(
                weapon_id=weapon_id,
                skin_id=skin_id,
                quality_id=quality_id,
                stattrak_existence=stattrak_existence,
            )
        raise BotDbException(
            ENTITY_NOT_FOUND_ERROR_MSG.format(
                entity="Relation",
                identifier="weapon_name, skin_name, quality_name",
                entity_identifier=f"{weapon_name}, {skin_name}, {quality_name}",
            ),
        )

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(entity="Relation", fields="name")
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Relation",
                    identifier=identifier,
                    entity_identifier=entity_identifier,
                )
            ) from exc
