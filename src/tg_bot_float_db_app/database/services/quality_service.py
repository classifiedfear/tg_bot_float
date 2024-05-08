from typing import List

import sqlalchemy

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_common_dtos.quality_dto import QualityDTO


class QualityService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, quality_dto: QualityDTO) -> QualityModel:
        quality_model = QualityModel(**quality_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(quality_model)
        await self._commit_and_rollback_if_errors()
        return quality_model

    async def get_by_id(self, quality_id: int) -> QualityModel | None:
        return await self._session.get(QualityModel, quality_id)

    async def update_by_id(self, quality_id: int, quality_dto: QualityDTO) -> QualityModel | None:
        update_stmt = sqlalchemy.update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.id == quality_id)
        returning_stmt = where_stmt.returning(QualityModel)
        quality_model = await self._session.scalar(returning_stmt)
        if quality_model is not None:
            await self._commit_and_rollback_if_errors()
        return quality_model

    async def delete_by_id(self, quality_id: int) -> None:
        delete_stmt = sqlalchemy.delete(QualityModel).where(QualityModel.id == quality_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException("There are no row with this id!")
        await self._commit_and_rollback_if_errors()

    async def create_many(self, quality_dtos: List[QualityDTO]) -> List[QualityModel]:
        quality_models = [
            QualityModel(**quality_post_model.model_dump(exclude_none=True, exclude={"id"}))
            for quality_post_model in quality_dtos
        ]
        self._session.add_all(quality_models)
        await self._commit_and_rollback_if_errors()
        return quality_models

    async def get_many_by_id(self, ids: List[int]) -> sqlalchemy.ScalarResult[QualityModel]:
        select_stmt = sqlalchemy.select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(
        self, quality_names: List[str]
    ) -> sqlalchemy.ScalarResult[QualityModel]:
        select_stmt = sqlalchemy.select(QualityModel)
        where_stmt = select_stmt.where(QualityModel.name.in_(quality_names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, quality_ids: List[int]) -> None:
        delete_stmt = sqlalchemy.delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.id.in_(quality_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(quality_ids):
            raise BotDbDeleteException(
                "Number of deleted rows does not match the requested rows for deletion!"
            )
        await self._commit_and_rollback_if_errors()

    async def delete_many_by_name(self, quality_names: List[str]) -> None:
        delete_stmt = sqlalchemy.delete(QualityModel)
        where_stmt = delete_stmt.where(QualityModel.name.in_(quality_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(quality_names):
            raise BotDbDeleteException(
                "Number of deleted rows does not match the requested rows for deletion!"
            )
        await self._commit_and_rollback_if_errors()

    async def upsert(self, quality_dto: QualityDTO) -> QualityModel | None:
        values = quality_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = postgresql.insert(QualityModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(QualityModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> QualityModel | None:
        stmt = sqlalchemy.select(QualityModel).where(QualityModel.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(
        self, quality_name: str, quality_dto: QualityDTO
    ) -> QualityModel | None:
        update_stmt = sqlalchemy.update(QualityModel).values(
            **quality_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(QualityModel.name == quality_name)
        returning_stmt = where_stmt.returning(QualityModel)
        quality_model = await self._session.scalar(returning_stmt)
        if quality_model is not None:
            await self._commit_and_rollback_if_errors()
        return quality_model

    async def delete_by_name(self, quality_name: str) -> int:
        delete_stmt = sqlalchemy.delete(QualityModel).where(QualityModel.name == quality_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row:
            await self._commit_and_rollback_if_errors()
        return result.rowcount

    async def get_all(self) -> sqlalchemy.ScalarResult[QualityModel]:
        stmt = sqlalchemy.select(QualityModel)
        return await self._session.scalars(stmt)

    async def _commit_and_rollback_if_errors(self) -> None:
        try:
            await self._session.commit()
        except:
            await self._session.rollback()
            raise
