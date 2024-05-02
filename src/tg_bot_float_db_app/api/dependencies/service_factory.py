from typing import Annotated

from fastapi import Depends

from tg_bot_float_db_app.database.db_factory import BotDbFactory
from tg_bot_float_db_app.database.bot_db_service_factory import BotDbServiceFactory

DbServiceFactory = Annotated[BotDbServiceFactory, Depends(BotDbFactory.get_service_factory)]