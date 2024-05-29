from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_db_app.misc.bot_db_exception import BotDbException
from tg_bot_float_db_app.misc.router_constants import ENTITY_FOUND_ERROR_MSG, NONE_FIELD_IN_ENTITY_ERROR_MSG


class SubscriptionService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, subscription_dto: SubscriptionDTO):
        subscription_model = SubscriptionModel(**subscription_dto.model_dump(exclude_none=True, exclude={"id"}))
        self._session.add(subscription_model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_bot_db_exception(exc, "user_id", str(subscription_dto.user_id))
        return subscription_model

    async def get_all(self) -> Page[SubscriptionModel]:
        stmt = select(SubscriptionModel)
        return await paginate(self._session, stmt)


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
                    entity="Subscription", identifier=identifier, entity_identifier=entity_identifier
                )
            ) from exc


