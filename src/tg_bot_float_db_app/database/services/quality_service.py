from typing import List

from sqlalchemy import update, select, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO


class QualityService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, quality_dto: QualityDTO) -> QualityModel:
        quality_model = QualityModel(**quality_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(quality_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(quality_dto.name))
        return quality_model

    async def get_by_id(self, quality_id: int) -> QualityModel:
        quality_model = await self._session.get(QualityModel, quality_id)
        if quality_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="id", entity_identifier=str(quality_id)
                ),
            )
        return quality_model

    async def update_by_id(self, quality_id: int, quality_dto: QualityDTO) -> None:
        update_stmt = update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.id == quality_id)
        try:
            result = await self._session.execute(where_stmt)
            row_update = result.rowcount
            if row_update == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Quality", identifier="id", entity_identifier=str(quality_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(quality_dto.name))
        await self._session.commit()

    async def delete_by_id(self, quality_id: int) -> None:
        delete_stmt = delete(QualityModel).where(QualityModel.id == quality_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="id", entity_identifier=str(quality_id)
                ),
            )
        await self._session.commit()

    async def create_many(self, quality_dtos: List[QualityDTO]) -> List[QualityModel]:
        quality_models = [
            QualityModel(**quality_post_model.model_dump(exclude_none=True, exclude={"id"}))
            for quality_post_model in quality_dtos
        ]
        self._session.add_all(quality_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            names = [quality_dto.name for quality_dto in quality_dtos if quality_dto.name]
            existing_qualities = await self.get_many_by_name(names)
            self._raise_bot_db_exception(
                exc, "names", ", ".join(quality.name for quality in existing_qualities)
            )
        return quality_models

    async def get_many_by_id(self, ids: List[int]) -> ScalarResult[QualityModel]:
        select_stmt = select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.id.in_(ids))
        quality_models = await self._session.scalars(where_stmt)
        return quality_models

    async def get_many_by_name(self, quality_names: List[str]) -> ScalarResult[QualityModel]:
        select_stmt = select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.name.in_(quality_names))
        quality_models = await self._session.scalars(where_stmt)
        return quality_models

    async def delete_many_by_id(self, quality_ids: List[int]) -> None:
        delete_stmt = delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.id.in_(quality_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(quality_ids):
            await self._session.rollback()
            existing_qualities = await self.get_many_by_id(quality_ids)
            existing_ids = {quality.id for quality in existing_qualities}
            non_existing_ids = set(quality_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality",
                    identifier="ids",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                ),
            )
        await self._session.commit()

    async def delete_many_by_name(self, quality_names: List[str]) -> None:
        delete_stmt = delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.name.in_(quality_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(quality_names):
            await self._session.rollback()
            existing_qualities = await self.get_many_by_name(quality_names)
            existing_names = {quality.name for quality in existing_qualities}
            non_existing_names = set(quality_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality",
                    identifier="ids",
                    entity_identifier=", ".join(name for name in non_existing_names),
                ),
            )
        await self._session.commit()

    async def upsert(self, quality_dto: QualityDTO) -> None:
        values = quality_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = insert(QualityModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(QualityModel)
        await self._session.execute(returning_stmt)
        await self._session.commit()

    async def get_by_name(self, quality_name: str) -> QualityModel:
        stmt = select(QualityModel).where(QualityModel.name == quality_name)
        quality_model = await self._session.scalar(stmt)
        if quality_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="id", entity_identifier=quality_name
                ),
            )
        return quality_model

    async def update_by_name(self, quality_name: str, quality_dto: QualityDTO) -> None:
        update_stmt = update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.name == quality_name)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Quality", identifier="name", entity_identifier=quality_name
                    )
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(quality_dto.name))
        await self._session.commit()

    async def delete_by_name(self, quality_name: str) -> None:
        delete_stmt = delete(QualityModel).where(QualityModel.name == quality_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="name", entity_identifier=quality_name
                )
            )
        await self._session.commit()

    async def get_all_paginated(self) -> Page[QualityDTO]:
        select_stmt = select(QualityModel)
        return await paginate(self._session, select_stmt)

    async def get_all(self) -> ScalarResult[QualityModel]:
        select_stmt = select(QualityModel)
        return await self._session.scalars(select_stmt)

    async def get_many_by_weapon_skin_name(self, weapon_name: str, skin_name: str):
        stmt = (
            select(QualityModel)
            .join(QualityModel.relations)
            .join(RelationModel.skin)
            .join(RelationModel.weapon)
            .where(WeaponModel.name == weapon_name, SkinModel.name == skin_name)
        )
        return await self._session.scalars(stmt)

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(
                    entity="Quality", fields="name, stattrak_existence"
                )
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier=identifier, entity_identifier=entity_identifier
                )
            ) from exc
