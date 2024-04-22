from tg_bot_float_db_app.database.bot_database_context import BotDatabaseContext
from tg_bot_float_db_app.database.bot_database_engine import BotDatabaseEngine

url = (
            f'postgresql+asyncpg://'
            f'classified:rv9up0ax@192.168.0.200:5432'
            f'/tg_bot_float_db'
        )
engine = BotDatabaseEngine(url)


async def get_db_context():
    async with BotDatabaseContext(engine) as context:
        yield context


async def get_db_weapon_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_weapon_context()


async def get_db_skin_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_skin_context()


async def get_db_quality_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_quality_context()


async def get_db_wsq_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_weapon_skin_quality_table()


async def get_db_user_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_user_context()


async def get_db_subscription_context():
    async with BotDatabaseContext(engine) as database:
        yield
        