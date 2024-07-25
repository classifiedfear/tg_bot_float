from sqlalchemy import ScalarResult, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_db_app.database.models.user_model import UserModel
from tg_bot_float_db_app.bot_db_exception import BotDbException
from tg_bot_float_db_app.db_app_constants import (
    ENTITY_FOUND_ERROR_MSG,
    ENTITY_NOT_FOUND_ERROR_MSG,
    NONE_FIELD_IN_ENTITY_ERROR_MSG,
)


class SubscriptionService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, subscription_dto: SubscriptionDTO) -> SubscriptionModel:
        subscription_model = SubscriptionModel(
            **subscription_dto.model_dump(exclude_none=True, exclude={"id"})
        )
        self._session.add(subscription_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "user_id", str(subscription_dto.user_id))
        return subscription_model

    async def get_subscription(
        self, telegram_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool
    ) -> SubscriptionModel:
        select_stmt = select(SubscriptionModel).join(UserModel)
        where_stmt = select_stmt.where(
            SubscriptionModel.weapon_id == weapon_id,
            SubscriptionModel.skin_id == skin_id,
            SubscriptionModel.quality_id == quality_id,
            SubscriptionModel.stattrak == stattrak,
            UserModel.telegram_id == telegram_id,
        )
        subscription_model = await self._session.scalar(where_stmt)
        if subscription_model is None:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User",
                    identifier="telegram_id, weapon_id, skin_id, quality_id, stattrak",
                    entity_identifier=f"{telegram_id}, {weapon_id}, {skin_id}, {quality_id}, {stattrak}",
                ),
            )
        return subscription_model

    async def delete(
        self, telegram_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool
    ) -> None:
        delete_stmt = delete(SubscriptionModel)
        where_stmt = delete_stmt.where(
            SubscriptionModel.weapon_id == weapon_id,
            SubscriptionModel.skin_id == skin_id,
            SubscriptionModel.quality_id == quality_id,
            SubscriptionModel.stattrak == stattrak,
            UserModel.telegram_id == telegram_id,
        )
        result = await self._session.execute(where_stmt)
        deleted_row = result.rowcount
        if deleted_row == 0:
            raise BotDbException(
                ENTITY_NOT_FOUND_ERROR_MSG.format(
                    entity="User",
                    identifier="telegram_id, weapon_id, skin_id, quality_id, stattrak",
                    entity_identifier=f"{telegram_id}, {weapon_id}, {skin_id}, {quality_id}, {stattrak}",
                ),
            )
        await self._session.commit()

    async def get_valuable_subscriptions(self) -> Page[SubscriptionToFindDTO]:
        select_stmt = (
            select(
                SubscriptionModel.weapon_id,
                SubscriptionModel.skin_id,
                SubscriptionModel.quality_id,
                SubscriptionModel.stattrak,
                func.count("*").label("count"),
            )
            .select_from(SubscriptionModel)
            .group_by(
                SubscriptionModel.weapon_id,
                SubscriptionModel.skin_id,
                SubscriptionModel.quality_id,
                SubscriptionModel.stattrak,
            )
            .order_by(desc("count"))
        )
        return await paginate(self._session, select_stmt)

    async def get_all(self) -> ScalarResult[SubscriptionModel]:
        select_stmt = select(SubscriptionModel)
        return await self._session.scalars(select_stmt)

    async def get_all_paginated(self) -> Page[SubscriptionModel]:
        select_stmt = select(SubscriptionModel)
        return await paginate(self._session, select_stmt)

    async def get_subscriptions_by_telegram_id(self, telegram_id: int):
        select_stmt = select(SubscriptionModel).join(UserModel)
        where_stmt = select_stmt.where(UserModel.telegram_id == telegram_id)
        return await self._session.scalars(where_stmt)

    async def get_subscriptions_by_telegram_id_paginated(
        self, telegram_id: int
    ) -> Page[SubscriptionModel]:
        select_stmt = select(SubscriptionModel).join(UserModel)
        where_stmt = select_stmt.where(UserModel.telegram_id == telegram_id)
        return await paginate(self._session, where_stmt)

    def _raise_bot_db_exception(
        self,
        exc: IntegrityError,
        identifier: str,
        entity_identifier: str,
    ) -> None:
        exc_msg = str(exc.orig)
        if "NotNullViolationError" in exc_msg:
            raise BotDbException(
                NONE_FIELD_IN_ENTITY_ERROR_MSG.format(entity="Subscription", fields="user_id")
            ) from exc
        if "UniqueViolationError" in exc_msg:
            raise BotDbException(
                ENTITY_FOUND_ERROR_MSG.format(
                    entity="Subscription",
                    identifier=identifier,
                    entity_identifier=entity_identifier,
                )
            ) from exc
