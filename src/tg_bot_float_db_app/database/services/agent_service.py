from typing import List
from sqlalchemy import select, update, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.database.models.agent_model import AgentModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)


class AgentService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, agent_dto: AgentDTO) -> AgentModel:
        agent_model = AgentModel(**agent_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(agent_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(agent_model.name))
        return agent_model

    async def get_by_id(self, agent_id: int) -> AgentModel:
        agent_model = await self._session.get(AgentModel, agent_id)
        if agent_model is None:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Agent", identifier="id", entity_edentifier=str(agent_id)
                )
            )
        return agent_model

    async def update_by_id(self, agent_id: int, agent_dto: AgentDTO) -> None:
        update_stmt = update(AgentModel).values(
            **agent_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(AgentModel.id == agent_id)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Agent", identifier="id", entity_identifier=str(agent_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(agent_dto.name))
        else:
            await self._session.commit()

    async def delete_by_id(self, agent_id: int) -> None:
        delete_stmt = delete(AgentModel).where(AgentModel.id == agent_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Agent", identifier="id", entity_identifier=str(agent_id)
                )
            )
        await self._session.commit()

    async def create_many(self, agent_dtos: List[AgentDTO]) -> List[AgentModel]:
        agent_models = [
            AgentModel(**agent_post_model.model_dump(exclude_none=True, exclude={"id"}))
            for agent_post_model in agent_dtos
        ]
        self._session.add_all(agent_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            names = [agent_dto.name for agent_dto in agent_dtos if agent_dto.name]
            existence_agent_db_models = await self.get_many_by_name(names)
            self._raise_bot_db_exception(
                exc, "names", ", ".join(agent.name for agent in existence_agent_db_models)
            )

        return agent_models

    async def get_many_by_id(self, agent_ids: List[int]) -> ScalarResult[AgentModel]:
        select_stmt = select(AgentModel)
        where_stmt = select_stmt.where(AgentModel.id.in_(agent_ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_id_paginated(self, agent_ids: List[int]) -> Page[AgentModel]:
        select_stmt = select(AgentModel)
        where_stmt = select_stmt.where(AgentModel.id.in_(agent_ids))
        return await paginate(self._session, where_stmt)

    async def get_many_by_name(self, agent_names: List[str]) -> ScalarResult[AgentModel]:
        select_stmt = select(AgentModel)
        where_stmt = select_stmt.where(AgentModel.name.in_(agent_names))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name_paginated(self, agent_names: List[str]) -> Page[AgentModel]:
        select_stmt = select(AgentModel)
        where_stmt = select_stmt.where(AgentModel.name.in_(agent_names))
        return await paginate(self._session, where_stmt)

    async def delete_many_by_id(self, agent_ids: List[int]) -> None:
        delete_stmt = delete(AgentModel)
        where_stmt = delete_stmt.where(AgentModel.id.in_(agent_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(agent_ids):
            await self._session.rollback()
            existing_agents = await self.get_many_by_id(agent_ids)
            existing_ids = {agent.id for agent in existing_agents}
            non_existing_ids = set(agent_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Agent",
                    identifier="id",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                )
            )
        await self._session.commit()

    async def delete_many_by_name(self, agent_names: List[str]) -> None:
        delete_stmt = delete(AgentModel)
        where_stmt = delete_stmt.where(AgentModel.name.in_(agent_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(agent_names):
            await self._session.rollback()
            existing_agents = await self.get_many_by_name(agent_names)
            existing_names = {agent.name for agent in existing_agents}
            non_existing_names = set(agent_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Agent",
                    identifier="id",
                    entity_identifier=", ".join(name for name in non_existing_names),
                ),
            )
        await self._session.commit()

    async def upsert(self, agent_dto: AgentDTO) -> AgentDTO | None:
        values = agent_dto.model_dump(exclude_none=True, exclude={"id"})
        insert_stmt = insert(AgentModel).values(**values)
        do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(AgentModel)
        await self._session.execute(returning_stmt)
        await self._session.commit()

    async def get_by_name(self, agent_name: str) -> AgentModel:
        select_stmt = select(AgentModel).where(AgentModel.name == agent_name)
        agent_model = await self._session.scalar(select_stmt)
        if agent_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Agent", identifier="name", entity_identifier=agent_name
                )
            )
        return agent_model

    async def update_by_name(self, agent_name: str, agent_dto: AgentDTO) -> None:
        update_stmt = update(AgentModel).values(
            **agent_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(AgentModel.name == agent_name)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        enitity="Agent", identifier="name", entity_identifier=agent_name
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", agent_name)
        await self._session.commit()

    async def delete_by_name(self, agent_name: str) -> None:
        delete_stmt = delete(AgentModel).where(AgentModel.name == agent_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Agent", identifier="name", entity_identifier=agent_name
                ),
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[AgentModel]:
        select_stmt = select(AgentModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[AgentModel]:
        select_stmt = select(AgentModel)
        return await paginate(self._session, select_stmt)

    async def update_relations(self, agent_model: AgentModel, skin_models: List[SkinModel]) -> None:
        agent_model.skins.extend(skin_models)
        await self._session.commit()

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(entity="Weapon", fields="name")
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier=identifier, entity_identifier=entity_identifier
                )
            ) from exc
