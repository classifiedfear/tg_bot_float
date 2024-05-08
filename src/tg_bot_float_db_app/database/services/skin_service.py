from typing import List

from sqlalchemy import ScalarResult, select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_common_dtos.skin_dto import SkinDTO


class SkinService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, skin_dto: SkinDTO) -> SkinModel:
        skin_model = SkinModel(**skin_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(skin_model)
        await self._commit_and_rollback_if_errors()
        return skin_model

    async def get_by_id(self, skin_id: int) -> SkinModel | None:
        return await self._session.get(SkinModel, skin_id)

    async def update_by_id(self, skin_id: int, skin_dto: SkinDTO) -> SkinModel | None:
        update_stmt = update(SkinModel).values(
            **skin_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(SkinModel.id == skin_id)
        returning_stmt = where_stmt.returning(SkinModel)
        skin = await self._session.scalar(returning_stmt)
        if skin is not None:
            await self._commit_and_rollback_if_errors()
        return skin

    async def delete_by_id(self, skin_id: int) -> None:
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.id == skin_id)
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def create_many(self, skin_dtos: List[SkinDTO]) -> List[SkinModel]:
        skin_models = [
            SkinModel(**skin_dto.model_dump(exclude_none=True, exclude={"id"}))
            for skin_dto in skin_dtos
        ]
        self._session.add_all(skin_models)
        await self._commit_and_rollback_if_errors()
        return skin_models

    async def get_many_by_id(self, ids: List[int]):
        select_stmt = select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, skin_names: List[str]):
        select_stmt = select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.name.in_(skin_names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: List[int]) -> None:
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.id.in_(ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(ids):
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def delete_many_by_name(self, skin_names: List[str]):
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.name.in_(skin_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(skin_names):
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def upsert(self, skin_dto: SkinDTO):
        values = skin_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = insert(SkinModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(SkinModel)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> SkinModel | None:
        stmt = select(SkinModel).where(SkinModel.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, name: str, skin_dto: SkinDTO) -> SkinModel | None:
        update_stmt = update(SkinModel).values(
            **skin_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(SkinModel.name == name)
        returning_stmt = where_stmt.returning(SkinModel)
        skin_model = await self._session.scalar(returning_stmt)
        if skin_model is not None:
            await self._commit_and_rollback_if_errors()
        return skin_model

    async def delete_by_name(self, skin_name: str) -> None:
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.name == skin_name)
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row != 1:
            raise BotDbDeleteException
        await self._commit_and_rollback_if_errors()

    async def get_all(self) -> ScalarResult[SkinModel]:
        stmt = select(SkinModel)
        return await self._session.scalars(stmt)

    async def _commit_and_rollback_if_errors(self) -> None:
        try:
            await self._session.commit()
        except:
            await self._session.rollback()
            raise
