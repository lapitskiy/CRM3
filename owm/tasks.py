from .models import parser_table, crontab_table
import asyncio
from crm3.celery import app
from .utils import autoupdate_sync_inventory
from sqlalchemy.future import select
from crm3.utils_db import AsyncSessionLocal


@app.task
def sync_inventory_owm():
    """
    Основная задача, которая диспетчеризует асинхронные задачи для всех активных cron.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        coroutine = run_sync_inventory()
        task = loop.create_task(coroutine)
    else:
        asyncio.run(run_sync_inventory())

async def run_sync_inventory():
    """
    Асинхронная обработка всех активных cron через SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Выполняем запрос для получения всех активных cron
            query = select(crontab_table).where(
                (crontab_table.c.name == "autoupdate") & (crontab_table.c.active == True)
            )
            result = await session.execute(query, execution_options={"prebuffer_rows": False})
            crontabs = result.fetchall()

            await session.commit()

            # Диспетчеризация задач для каждого cron
            for cron in crontabs:
                execute_autoupdate.delay(cron.id)

    return "All tasks dispatched"


@app.task
def execute_autoupdate(cron_id):
    """
    Обертка для запуска асинхронной задачи с использованием asyncio.run.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        coroutine = run_autoupdate(cron_id)
        task = loop.create_task(coroutine)
    else:
        asyncio.run(run_autoupdate(cron_id))


async def run_autoupdate(cron_id):
    """
    Асинхронная обработка одного cron через SQLAlchemy.
    """
    await autoupdate_sync_inventory(cron_id=cron_id)  # Асинхронная обработка




