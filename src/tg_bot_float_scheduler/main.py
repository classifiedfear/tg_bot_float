import asyncio


from tg_bot_float_scheduler.scheduler_service import SchedulerService
from tg_bot_float_scheduler.scheduler_settings import SchedulerSettings


def main() -> None:
    scheduler_settings = SchedulerSettings()
    scheduler_service = SchedulerService(scheduler_settings)
    await scheduler_service.schedule()


if __name__ == "__main__":
    asyncio.run(main())
