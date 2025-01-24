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

    async def _find_items_with_benefit_task(self) -> None:
        async with ClientSession() as session:
            async with session.get(self._scheduler_settings.sub_benefit_finder_url) as response:
                assert response.status == 200

    async def _add_tasks_to_scheduler(self, scheduler: AsyncScheduler) -> None:
        await scheduler.add_schedule(
            self._db_updater_task, CalendarIntervalTrigger(months=1, hour=10)
        )
        await scheduler.add_schedule(self._find_items_with_benefit_task, IntervalTrigger(minutes=3))

    async def schedule(self) -> None:
        async with AsyncScheduler(
            data_store=SQLAlchemyDataStore(self._scheduler_settings.db_url),
        ) as scheduler:
            await self._add_tasks_to_scheduler(scheduler)
            await scheduler.run_until_stopped()
