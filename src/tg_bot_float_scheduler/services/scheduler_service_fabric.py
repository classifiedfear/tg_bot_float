from tg_bot_float_scheduler.services.db_updater.db_data_updater_service import (
    DbDataUpdaterService,
)
from tg_bot_float_scheduler.services.db_updater.db_data_sender_service import DbDataSenderService
from tg_bot_float_scheduler.services.db_updater.db_source_data_getter_service import (
    DbSourceDataGetterService,
)

from tg_bot_float_scheduler.services.benefit_finder.source_data_getter_service import (
    SourceDataGetterService,
)
from tg_bot_float_scheduler.services.benefit_finder.benefit_finder_service import BenefitFinderService
from settings.scheduler_settings import SchedulerSettings


class SchedulerServiceFabric:
    def __init__(self, scheduler_settings: SchedulerSettings) -> None:
        self._scheduler_settings = scheduler_settings

    def get_db_updater(self) -> DbDataUpdaterService:
        db_source_data_getter = DbSourceDataGetterService(self._scheduler_settings)
        db_data_sender = DbDataSenderService(self._scheduler_settings)
        db_updater = DbDataUpdaterService(db_source_data_getter, db_data_sender)
        return db_updater

    def get_benefit_finder(self) -> BenefitFinderService:
        source_data_getter = SourceDataGetterService(self._scheduler_settings)
        steam_csm_matcher = BenefitFinderService(source_data_getter)
        return steam_csm_matcher
