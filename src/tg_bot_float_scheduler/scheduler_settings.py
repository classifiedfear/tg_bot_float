from pydantic_settings import BaseSettings, SettingsConfigDict


class SchedulerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_scheduler/scheduler_variables.env", env_file_encoding="utf-8"
    )

    db_updater: str
    db_url: str
    sub_benefit_finder_url: str
