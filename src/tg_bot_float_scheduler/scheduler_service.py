from aiohttp import ClientSession

from apscheduler import AsyncScheduler
from apscheduler.triggers.calendarinterval import CalendarIntervalTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from tg_bot_float_scheduler.scheduler_settings import SchedulerSettings


class SchedulerService:
    def __init__(self, scheduler_settings: SchedulerSettings) -> None:
        self._scheduler_settings = scheduler_settings

    async def _db_updater_task(self) -> None:
        async with ClientSession() as session:
            async with session.get(self._scheduler_settings.db_updater) as response:
                assert response.status == 200

    async def schedule(self) -> None:
        async with AsyncScheduler(
            data_store=SQLAlchemyDataStore(self._scheduler_settings.db_url),
        ) as scheduler:
            await scheduler.add_schedule(
                self._db_updater_task, CalendarIntervalTrigger(months=1, hour=10)
            )
            # await scheduler.add_schedule(benefit_finder.find_items_with_benefit, IntervalTrigger(minutes=3)) for future task
            await scheduler.run_until_stopped()
