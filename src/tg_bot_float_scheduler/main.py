import asyncio
from functools import lru_cache


from tg_bot_float_scheduler.scheduler_service import SchedulerService
from tg_bot_float_scheduler.scheduler_settings import SchedulerSettings


@lru_cache
def get_scheduler_settings() -> SchedulerSettings:
    return SchedulerSettings()  # type: ignore "Load variables from scheduler_variables.env file"


async def main() -> None:
    scheduler_settings = get_scheduler_settings()
    scheduler_service = SchedulerService(scheduler_settings)
    await scheduler_service.schedule()


if __name__ == "__main__":
    asyncio.run(main())
