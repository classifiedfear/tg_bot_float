from typing import List
from http import HTTPStatus

from sqlalchemy import update, select, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.misc.exceptions import BotDbException
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
)
from tg_bot_float_common_dtos.quality_dto import QualityDTO


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
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="name", entity_identifier=quality_dto.name
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
        return quality_model

    async def get_by_id(self, quality_id: int) -> QualityModel:
        quality_model = await self._session.get(QualityModel, quality_id)
        if quality_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="id", entity_identifier=str(quality_id)
                ),
                HTTPStatus.NOT_FOUND,
            )
        return quality_model

    async def update_by_id(self, quality_id: int, quality_dto: QualityDTO) -> QualityModel:
        update_stmt = update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.id == quality_id)
        returning_stmt = where_stmt.returning(QualityModel)
        try:
            if (quality_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Quality", identifier="id", entity_identifier=str(quality_id)
                    ),
                    HTTPStatus.NOT_FOUND,
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="name", entity_identifier=quality_dto.name
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
        await self._session.commit()
        return quality_model

    async def delete_by_id(self, quality_id: int) -> None:
        delete_stmt = delete(QualityModel).where(QualityModel.id == quality_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="id", entity_identifier=str(quality_id)
                ),
                HTTPStatus.NOT_FOUND,
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
            existence_quality_db_models = await self.get_many_by_name(names)
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Quality",
                    identifier="names",
                    entity_identifier=", ".join(
                        quality.name for quality in existence_quality_db_models
                    ),
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
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
            existence_quality_db_models = await self.get_many_by_id(quality_ids)
            existence_ids = {quality.id for quality in existence_quality_db_models}
            difference_ids = set(quality_ids).symmetric_difference(existence_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality",
                    identifier="ids",
                    entity_identifier=", ".join(str(id) for id in difference_ids),
                ),
                HTTPStatus.NOT_FOUND,
            )
        await self._session.commit()

    async def delete_many_by_name(self, quality_names: List[str]) -> None:
        delete_stmt = delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.name.in_(quality_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(quality_names):
            existence_quality_db_models = await self.get_many_by_name(quality_names)
            existence_names = {quality.name for quality in existence_quality_db_models}
            difference_names = set(quality_names).symmetric_difference(existence_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality",
                    identifier="names",
                    entity_identifier=", ".join(name for name in difference_names),
                ),
                HTTPStatus.NOT_FOUND,
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
                    entity="Quality", identifier="name", entity_identifier=quality_name
                ),
                HTTPStatus.NOT_FOUND,
            )
        return quality_model

    async def update_by_name(self, quality_name: str, quality_dto: QualityDTO) -> QualityModel:
        update_stmt = update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.name == quality_name)
        returning_stmt = where_stmt.returning(QualityModel)
        try:
            if (quality_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Quality", identifier="name", entity_identifier=quality_name
                    ),
                    HTTPStatus.NOT_FOUND,
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="name", entity_identifier=quality_dto.name
                ),
                HTTPStatus.BAD_REQUEST,
            ) from exc
        await self._session.commit()
        return quality_model

    async def delete_by_name(self, quality_name: str) -> None:
        delete_stmt = delete(QualityModel).where(QualityModel.name == quality_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Quality", identifier="name", entity_identifier=quality_name
                ),
                HTTPStatus.NOT_FOUND
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[QualityModel]:
        select_stmt = select(QualityModel)
        return await self._session.scalars(select_stmt)
