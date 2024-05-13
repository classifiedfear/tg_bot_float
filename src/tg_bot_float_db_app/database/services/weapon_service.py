from typing import List

from sqlalchemy import select, update, delete, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.misc.exceptions import BotDbException
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
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
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="name", entity_identifier=weapon_dto.name
                ),
            ) from exc
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

    async def update_by_id(self, weapon_id: int, weapon_dto: WeaponDTO) -> WeaponModel | None:
        update_stmt = update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.id == weapon_id)
        returning_stmt = where_stmt.returning(WeaponModel)
        try:
            if (weapon_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Weapon", identifier="id", entity_identifier=str(weapon_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="name", entity_identifier=weapon_dto.name
                ),
            ) from exc
        await self._session.commit()
        return weapon_model

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
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Weapon",
                    identifier="names",
                    entity_identifier=", ".join(
                        weapon.name for weapon in existence_weapon_db_models
                    ),
                ),
            ) from exc
        return weapon_models

    async def get_many_by_id(self, weapon_ids: List[int]):
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.id.in_(weapon_ids))
        weapon_models = await self._session.scalars(where_stmt)
        return weapon_models

    async def get_many_by_name(self, weapon_names: List[str]):
        select_stmt = select(WeaponModel)
        where_stmt = select_stmt.where(WeaponModel.name.in_(weapon_names))
        weapon_models = await self._session.scalars(where_stmt)
        return weapon_models

    async def delete_many_by_id(self, weapon_ids: List[int]) -> None:
        delete_stmt = delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.id.in_(weapon_ids))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(weapon_ids):
            existing_weapons = await self.get_many_by_id(weapon_ids)
            existing_ids = {weapon.id for weapon in existing_weapons}
            non_existing_ids = set(weapon_ids).symmetric_difference(existing_ids)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon",
                    identifier="ids",
                    entity_identifier=", ".join(str(id) for id in non_existing_ids),
                ),
            )
        await self._session.commit()

    async def delete_many_by_name(self, weapon_names: List[str]):
        delete_stmt = delete(WeaponModel)
        where_stmt = delete_stmt.where(WeaponModel.name.in_(weapon_names))
        result = await self._session.execute(where_stmt)
        deleted_rows = result.rowcount
        if deleted_rows != len(weapon_names):
            existing_weapons = await self.get_many_by_name(weapon_names)
            existing_names = {weapon.name for weapon in existing_weapons}
            non_existing_names = set(weapon_names).symmetric_difference(existing_names)
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="Weapon",
                    identifier="names",
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

    async def update_by_name(self, weapon_name: str, weapon_dto: WeaponDTO):
        update_stmt = update(WeaponModel).values(
            **weapon_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(WeaponModel.name == weapon_name)
        returning_stmt = where_stmt.returning(WeaponModel)
        try:
            if (weapon_model := await self._session.scalar(returning_stmt)) is None:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="Weapon", identifier="name", entity_identifier=weapon_name
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Weapon", identifier="name", entity_identifier=weapon_dto.name
                ),
            ) from exc
        await self._session.commit()
        return weapon_model

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
        stmt = select(WeaponModel)
        return await self._session.scalars(stmt)

    async def get_many_by_skin_name(self, skin_name: str) -> ScalarResult[WeaponModel]:
        stmt = (
            select(WeaponModel)
            .join(WeaponModel.relations)
            .join(RelationModel.skin)
            .where(SkinModel.name == skin_name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
