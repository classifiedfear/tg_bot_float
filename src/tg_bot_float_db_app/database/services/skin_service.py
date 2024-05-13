from typing import List

from sqlalchemy import ScalarResult, select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.misc.exceptions import BotDbException
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
)
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO


class SkinService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, skin_dto: SkinDTO) -> SkinModel:
        skin_model = SkinModel(**skin_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(skin_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="name", entity_identifier=skin_dto.name
                )
            ) from exc
        return skin_model

    async def get_by_id(self, skin_id: int) -> SkinModel:
        skin_model = await self._session.get(SkinModel, skin_id)
        if skin_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="id", entity_identifier=str(skin_id)
                ),
            )
        return skin_model

    async def update_by_id(self, skin_id: int, skin_dto: SkinDTO) -> SkinModel | None:
        update_stmt = update(SkinModel).values(
            **skin_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(SkinModel.id == skin_id)
        returning_stmt = where_stmt.returning(SkinModel)
        try:
            if (skin_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Skin", identifier="id", entity_identifier=str(skin_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="name", entity_identifier=skin_dto.name
                ),
            ) from exc
        await self._session.commit()
        return skin_model

    async def delete_by_id(self, skin_id: int) -> None:
        delete_stmt = delete(SkinModel).where(SkinModel.id == skin_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="id", entity_identifier=str(skin_id)
                ),
            )
        await self._session.commit()

    async def create_many(self, skin_dtos: List[SkinDTO]) -> List[SkinModel]:
        skin_models = [
            SkinModel(**skin_post_model.model_dump(exclude_none=True, exclude={"id"}))
            for skin_post_model in skin_dtos
        ]
        self._session.add_all(skin_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            names = [skin_dto.name for skin_dto in skin_dtos if skin_dto.name]
            existence_skin_db_models = await self.get_many_by_name(names)
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Skin",
                    identifier="names",
                    entity_identifier=", ".join(skin.name for skin in existence_skin_db_models),
                ),
            ) from exc
        return skin_models

    async def get_many_by_id(self, ids: List[int]):
        select_stmt = select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, skin_names: List[str]):
        select_stmt = select(SkinModel)
        where_stmt = select_stmt.where(SkinModel.name.in_(skin_names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, skin_ids: List[int]) -> None:
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.id.in_(skin_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(skin_ids):
            existing_skins = await self.get_many_by_id(skin_ids)
            existing_ids = {skin.id for skin in existing_skins}
            non_existing_ids = set(skin_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin",
                    identifier="ids",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                ),
            )
        await self._session.commit()

    async def delete_many_by_name(self, skin_names: List[str]):
        delete_stmt = delete(SkinModel)
        where_stmt = delete_stmt.where(SkinModel.name.in_(skin_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(skin_names):
            existing_skins = await self.get_many_by_name(skin_names)
            existing_names = {skin.name for skin in existing_skins}
            non_existing_names = set(skin_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin",
                    identifier="names",
                    entity_identifier=", ".join(name for name in non_existing_names),
                ),
            )
        await self._session.commit()

    async def upsert(self, skin_dto: SkinDTO):
        values = skin_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = insert(SkinModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(SkinModel)
        await self._session.execute(returning_stmt)
        await self._session.commit()

    async def get_by_name(self, skin_name: str) -> SkinModel:
        stmt = select(SkinModel).where(SkinModel.name == skin_name)
        skin_model = await self._session.scalar(stmt)
        if skin_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="name", entity_identifier=skin_name
                ),
            )
        return skin_model

    async def update_by_name(self, skin_name: str, skin_dto: SkinDTO) -> SkinModel | None:
        update_stmt = update(SkinModel).values(
            **skin_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(SkinModel.name == skin_name)
        returning_stmt = where_stmt.returning(SkinModel)
        try:
            if (skin_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Skin", identifier="name", entity_identifier=skin_name
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="name", entity_identifier=skin_dto.name
                ),
            ) from exc
        await self._session.commit()
        return skin_model

    async def delete_by_name(self, skin_name: str) -> None:
        delete_stmt = delete(SkinModel).where(SkinModel.name == skin_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Skin", identifier="name", entity_identifier=skin_name
                ),
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[SkinModel]:
        stmt = select(SkinModel)
        return await self._session.scalars(stmt)

    async def get_many_by_weapon_name(self, weapon_name: str) -> ScalarResult[SkinModel]:
        stmt = (
            select(SkinModel)
            .join(SkinModel.relations)
            .join(RelationModel.weapon)
            .where(WeaponModel.name == weapon_name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
