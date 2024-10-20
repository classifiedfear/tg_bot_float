from fastapi_pagination import Page
from sqlalchemy import delete, select, update, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_common_dtos.schema_dtos.user_dto import UserDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_db_app.database.models.user_model import UserModel
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_dto: UserDTO) -> UserModel:
        user_model = UserModel(**user_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(user_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "telegram_id", str(user_dto.telegram_id))
        return user_model

    async def get_by_id(self, user_id: int) -> UserModel:
        user_model = await self._session.get(UserModel, user_id)
        if user_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User", identifier="id", entity_identifier=str(user_id)
                ),
            )
        return user_model

    async def update_by_id(self, user_id: int, user_dto: UserDTO) -> None:
        update_stmt = update(UserModel).values(
            **user_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        where_stmt = update_stmt.where(UserModel.id == user_id)
        try:
            result = await self._session.execute(where_stmt)
            row_update = result.rowcount
            if row_update == 0:
                raise BotDbException(
                    ENTITY_NOT_FOUND_ERROR_MSG.format(
                        entity="User", identifier="id", entity_identifier=str(user_id)
                    ),
                )
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "telegram_id", str(user_dto.telegram_id))
        await self._session.commit()

    async def delete_by_id(self, user_id: int) -> None:
        delete_stmt = delete(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User", identifier="id", entity_identifier=str(user_id)
                ),
            )
        await self._session.commit()

    async def get_by_telegram_id(self, user_telegram_id: int) -> UserModel:
        stmt = select(UserModel).where(UserModel.telegram_id == user_telegram_id)
        quality_model = await self._session.scalar(stmt)
        if quality_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User", identifier="telegram_id", entity_identifier=str(user_telegram_id)
                ),
            )
        return quality_model

    async def delete_by_telegram_id(self, user_telegram_id: int) -> None:
        delete_stmt = delete(UserModel).where(UserModel.telegram_id == user_telegram_id)
        result = await self._session.execute(delete_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User", identifier="telegram_id", entity_identifier=str(user_telegram_id)
                )
            )
        await self._session.commit()

    async def get_all(self) -> ScalarResult[UserModel]:
        select_stmt = select(UserModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[UserModel]:
        select_stmt = select(UserModel)
        return await paginate(self._session, select_stmt)

    async def get_users_by_subcription(
        self, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool
    ):
        select_stmt = select(UserModel.telegram_id).join(UserModel.subscriptions)
        where_stmt = select_stmt.where(
            SubscriptionModel.weapon_id == weapon_id,
            SubscriptionModel.skin_id == skin_id,
            SubscriptionModel.quality_id == quality_id,
            SubscriptionModel.stattrak == stattrak,
        )
        return await self._session.scalars(where_stmt)

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(entity="User", fields="telegram_id")
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="User", identifier=identifier, entity_identifier=entity_identifier
                )
            ) from exc
