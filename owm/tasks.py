from .models import Crontab
import asyncio
from crm3.celery import app
from .utils import autoupdate_sync_inventory

from .models import Crontab
import asyncio
from crm3.celery import app
from .utils import autoupdate_sync_inventory


@app.task
def sync_inventory_owm():
    """
    Основная задача, которая диспетчеризует асинхронные задачи для всех активных cron.
    """
    asyncio.run(run_sync_inventory())

async def run_sync_inventory():
    """
    Асинхронная обработка всех активных cron через SQLAlchemy.
    """
    metadata = MetaData()
    async with AsyncSessionLocal() as session:
        # Отражаем структуру базы данных
        await session.run_sync(metadata.reflect, bind=session.bind)

        # Доступ к таблице Crontab
        crontab_table = metadata.tables["app_crontab"]

        # Выполняем запрос для получения всех активных cron
        query = select(crontab_table).where(
            (crontab_table.c.name == "autoupdate") & (crontab_table.c.active == True)
        )
        result = await session.execute(query)
        crontabs = result.fetchall()

        # Диспетчеризация задач для каждого cron
        for cron in crontabs:
            execute_autoupdate.delay(cron.id)

    return "All tasks dispatched"


@app.task
def execute_autoupdate(cron_id):
    """
    Обертка для запуска асинхронной задачи с использованием asyncio.run.
    """
    asyncio.run(run_autoupdate(cron_id))


async def run_autoupdate(cron_id):
    """
    Асинхронная обработка одного cron через SQLAlchemy.
    """
    await autoupdate_sync_inventory(cron_id=cron_id)  # Асинхронная обработка




