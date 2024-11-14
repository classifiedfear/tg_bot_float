from typing import List

from sqlalchemy import select, update, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.database.models.glove_model import GloveModel
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)


class GloveService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, glove_dto: GloveDTO) -> GloveModel:
        glove_model = GloveModel(**glove_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(glove_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(glove_dto.name))
        return glove_model

    async def get_by_id(self, glove_id: int) -> GloveModel:
        glove_model = await self._session.get(GloveModel, glove_id)
        if glove_model is None:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Glove", identifier="id", entity_identifier=str(glove_id)
                )
            )
        return glove_model

    async def update_by_id(self, glove_id: int, glove_dto: GloveDTO) -> None:
        update_stmt = update(GloveModel).values(
            **glove_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(GloveModel.id == glove_id)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Glove", identifier="id", entity_identifier=str(glove_id)
                    )
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(glove_dto.name))
        else:
            await self._session.commit()

    async def delete_by_id(self, glove_id: int) -> None:
        delete_stmt = delete(GloveModel)
        where_stmt = delete_stmt.where(GloveModel.id == glove_id)
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Glove", identifier="id", entity_identifier=str(glove_id)
                )
            )
        await self._session.commit()

    async def create_many(self, glove_dtos: List[GloveDTO]) -> List[GloveModel]:
        glove_models = [
            GloveModel(**glove_dto.model_dump(exclude_none=True, exclude={"id"}))
            for glove_dto in glove_dtos
        ]
        self._session.add_all(glove_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            names = [glove_dto.name for glove_dto in glove_dtos if glove_dto.name]
            existence_weapon_db_models = await self.get_many_by_name(names)
            self._raise_bot_db_exception(
                exc, "name", ", ".join(glove.name for glove in existence_weapon_db_models)
            )

        return glove_models

    async def get_many_by_id(self, ids: List[int]) -> ScalarResult[GloveModel]:
        select_stmt = select(GloveModel)
        where_stmt = select_stmt.where(GloveModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_id_paginated(self, ids: List[int]) -> Page[GloveModel]:
        select_stmt = select(GloveModel)
        where_stmt = select_stmt.where(GloveModel.name.in_(ids))
        return await paginate(self._session, where_stmt)

    async def get_many_by_name(self, names: List[str]) -> ScalarResult[GloveModel]:
        select_stmt = select(GloveModel)
        where_stmt = select_stmt.where(GloveModel.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name_paginated(self, glove_names: List[str]) -> Page[GloveModel]:
        select_stmt = select(GloveModel)
        where_stmt = select_stmt.where(GloveModel.name.in_(glove_names))
        return await paginate(self._session, where_stmt)

    async def delete_many_by_id(self, glove_ids: List[int]) -> None:
        delete_stmt = delete(GloveModel)
        where_stmt = delete_stmt.where(GloveModel.id.in_(glove_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(glove_ids):
            await self._session.rollback()
            existing_gloves = await self.get_many_by_id(glove_ids)
            existing_ids = {glove.id for glove in existing_gloves}
            non_existing_ids = set(glove_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Glove",
                    identifier="id",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                ),
            )
        await self._session.commit()

    async def delete_many_by_name(self, glove_names: List[str]) -> None:
        delete_stmt = delete(GloveModel)
        where_stmt = delete_stmt.where(GloveModel.name.in_(glove_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(glove_names):
            await self._session.rollback()
            existing_gloves = await self.get_many_by_name(glove_names)
            existing_names = {glove.name for glove in existing_gloves}
            non_existing_names = set(glove_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Glove",
                    identifier="id",
                    entity_identifier=", ".join(name for name in non_existing_names),
                ),
            )
        await self._session.commit()

    async def upsert(self, glove_dto: GloveDTO) -> GloveModel | None:
        values = glove_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = insert(GloveModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(GloveModel)
        await self._session.execute(returning_stmt)
        await self._session.commit()

    async def get_by_name(self, glove_name: str) -> GloveModel:
        stmt = select(GloveModel).where(GloveModel.name == glove_name)
        glove_model = await self._session.scalar(stmt)
        if glove_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Glove", identifier="name", entity_identifier=glove_name
                ),
            )
        return glove_model

    async def update_by_name(self, glove_name: str, glove_dto: GloveDTO) -> None:
        update_stmt = update(GloveModel).values(
            **glove_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(GloveModel.name == glove_name)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Glove", identifier="name", entity_identifier=glove_name
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", glove_name)
        await self._session.commit()

    async def delete_by_name(self, glove_name: str) -> None:
        delete_stmt = delete(GloveModel).where(GloveModel.name == glove_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Glove", identifier="name", entity_identifier=glove_name
                ),
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[GloveModel]:
        select_stmt = select(GloveModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[GloveModel]:
        select_stmt = select(GloveModel)
        return await paginate(self._session, select_stmt)

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(entity="Glove", fields="name")
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Glove", identifier=identifier, entity_identifier=entity_identifier
                )
            ) from exc
