import asyncio

from apscheduler import AsyncScheduler
from apscheduler.triggers.calendarinterval import CalendarIntervalTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from tg_bot_float_scheduler.services.scheduler_service_fabric import SchedulerServiceFabric
from settings.db_settings import DBSettings
from settings.scheduler_settings import SchedulerSettings


class SchedulerApp:
    def __init__(self) -> None:
        self._scheduler_settings = SchedulerSettings()
        self._db_settings = DBSettings()

    async def main(self) -> None:
        scheduler_service_fabric = SchedulerServiceFabric(self._scheduler_settings)
        db_updater = scheduler_service_fabric.get_db_updater()
        benefit_finder = scheduler_service_fabric.get_benefit_finder()
        async with AsyncScheduler(
            data_store=SQLAlchemyDataStore.from_url(self._db_settings.url),
        ) as scheduler:
            await scheduler.add_schedule(db_updater.update, CalendarIntervalTrigger(months=1, hour=10))
            await scheduler.add_schedule(benefit_finder.find_items_with_benefit, IntervalTrigger(minutes=3))
            await scheduler.run_until_stopped()


if __name__ == "__main__":
    scheduler_app = SchedulerApp()
    asyncio.run(scheduler_app.main())
