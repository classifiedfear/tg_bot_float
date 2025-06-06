from typing import List

from sqlalchemy import select, update, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class WeaponService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, weapon_dto: WeaponDTO) -> WeaponModel:
        weapon_model = WeaponModel(**weapon_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(weapon_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(weapon_dto.name))
        return weapon_model

    async def get_by_id(self, weapon_id: int) -> WeaponModel:
        weapon_model = await self._session.get(WeaponModel, weapon_id)
        if weapon_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="id", entity_identifier=str(weapon_id)
                ),
            )
        return weapon_model

    async def update_by_id(self, weapon_id: int, weapon_dto: WeaponDTO) -> None:
        update_stmt = update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.id == weapon_id)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Weapon", identifier="id", entity_identifier=str(weapon_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", str(weapon_dto.name))
        else:
            await self._session.commit()

    async def delete_by_id(self, weapon_id: int) -> None:
        delete_stmt = delete(WeaponModel).where(WeaponModel.id == weapon_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="id", entity_identifier=str(weapon_id)
                ),
            )
        await self._session.commit()

    async def create_many(self, weapon_dtos: List[WeaponDTO]) -> List[WeaponModel]:
        weapon_models = [
            WeaponModel(**weapon_post_model.model_dump(exclude_none=True, exclude={"id"}))
            for weapon_post_model in weapon_dtos
        ]
        self._session.add_all(weapon_models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            names = [weapon_dto.name for weapon_dto in weapon_dtos if weapon_dto.name]
            existence_weapon_db_models = await self.get_many_by_name(names)
            self._raise_bot_db_exception(
                exc, "names", ", ".join(weapon.name for weapon in existence_weapon_db_models)
            )

        return weapon_models

    async def get_many_by_id(self, weapon_ids: List[int]) -> ScalarResult[WeaponModel]:
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.id.in_(weapon_ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_id_paginated(self, weapon_ids: List[int]) -> Page[WeaponModel]:
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.id.in_(weapon_ids))
        return await paginate(self._session, where_stmt)

    async def get_many_by_name(self, weapon_names: List[str]) -> ScalarResult[WeaponModel]:
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.name.in_(weapon_names))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name_paginated(self, weapon_names: List[str]) -> Page[WeaponModel]:
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.name.in_(weapon_names))
        return await paginate(self._session, where_stmt)

    async def delete_many_by_id(self, weapon_ids: List[int]) -> None:
        delete_stmt = delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.id.in_(weapon_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(weapon_ids):
            await self._session.rollback()
            existing_weapons = await self.get_many_by_id(weapon_ids)
            existing_ids = {weapon.id for weapon in existing_weapons}
            non_existing_ids = set(weapon_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon",
                    identifier="id",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                ),
            )
        await self._session.commit()

    async def delete_many_by_name(self, weapon_names: List[str]) -> None:
        delete_stmt = delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.name.in_(weapon_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(weapon_names):
            await self._session.rollback()
            existing_weapons = await self.get_many_by_name(weapon_names)
            existing_names = {weapon.name for weapon in existing_weapons}
            non_existing_names = set(weapon_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon",
                    identifier="id",
                    entity_identifier=", ".join(name for name in non_existing_names),
                ),
            )
        await self._session.commit()

    async def upsert(self, weapon_dto: WeaponDTO) -> WeaponDTO | None:
        values = weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        stmt = insert(WeaponModel).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=values)
        returning_stmt = do_update_stmt.returning(WeaponModel)
        await self._session.execute(returning_stmt)
        await self._session.commit()

    async def get_by_name(self, weapon_name: str) -> WeaponModel:
        stmt = select(WeaponModel).where(WeaponModel.name == weapon_name)
        weapon_model = await self._session.scalar(stmt)
        if weapon_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="name", entity_identifier=weapon_name
                ),
            )
        return weapon_model

    async def update_by_name(self, weapon_name: str, weapon_dto: WeaponDTO) -> None:
        update_stmt = update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.name == weapon_name)
        try:
            result = await self._session.execute(where_stmt)
            row_updated = result.rowcount
            if row_updated == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Weapon", identifier="name", entity_identifier=weapon_name
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "name", weapon_name)
        await self._session.commit()

    async def delete_by_name(self, weapon_name: str) -> None:
        delete_stmt = delete(WeaponModel).where(WeaponModel.name == weapon_name)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="name", entity_identifier=weapon_name
                ),
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[WeaponModel]:
        select_stmt = select(WeaponModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[WeaponModel]:
        select_stmt = select(WeaponModel)
        return await paginate(self._session, select_stmt)

    async def get_many_by_skin_name(self, skin_name: str) -> ScalarResult[WeaponModel]:
        select_stmt = select(WeaponModel).join(WeaponModel.relations).join(RelationModel.skin)
        where_stmt = select_stmt.where(SkinModel.name == skin_name)
        without_duplicate_stmt = where_stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)

    async def get_many_by_skin_name_paginated(self, skin_name: str) -> Page[WeaponModel]:
        select_stmt = select(WeaponModel).join(WeaponModel.relations).join(RelationModel.skin)
        where_stmt = select_stmt.where(SkinModel.name == skin_name)
        without_duplicate_stmt = where_stmt.distinct()
        return await paginate(self._session, without_duplicate_stmt)

    async def get_many_by_skin_id(self, skin_id: int) -> ScalarResult[WeaponModel]:
        select_stmt = select(WeaponModel).join(WeaponModel.relations).join(RelationModel.skin)
        where_stmt = select_stmt.where(SkinModel.id == skin_id)
        without_duplicate_stmt = where_stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)

    async def get_many_by_skin_id_paginated(self, skin_id: int) -> Page[WeaponModel]:
        select_stmt = select(WeaponModel).join(WeaponModel.relations).join(RelationModel.skin)
        where_stmt = select_stmt.where(SkinModel.id == skin_id)
        without_duplicate_stmt = where_stmt.distinct()
        return await paginate(self._session, without_duplicate_stmt)

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
