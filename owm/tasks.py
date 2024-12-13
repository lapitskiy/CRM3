from eventlet import monkey_patch
monkey_patch()
import asyncio

from .models import parser_table, crontab_table
from crm3.celery import app
from .utils import autoupdate_sync_inventory
from sqlalchemy.future import select
from crm3.utils_db import AsyncSessionLocal, engine
from asgiref.sync import async_to_sync
from sqlalchemy.sql import join
from sqlalchemy.schema import MetaData
import aiohttp
import contextlib

@app.task
def sync_inventory_owm():
    """
    Основная задача, которая диспетчеризует асинхронные задачи для всех активных cron.
    """
    print('Starting sync_inventory_owm...')
    result = async_to_sync(run_sync_inventory)()  # Запуск корутины синхронно
    print('sync_inventory_owm completed.')
    return result


#@app.task(name="run_sync_inventory", bind=True)
#async def run_sync_inventory(self):



async def run_sync_inventory():
    """
    Асинхронная обработка всех активных cron через SQLAlchemy.
    """
    print('Fetching cron jobs...')

    async with get_db_session() as session:
        query = select(crontab_table).where(
            (crontab_table.c.name == "autoupdate") & (crontab_table.c.active == True)
        )
        result = await session.execute(query)
        crontabs = result.fetchall()

    # Создаем задачи для каждого cron
    tasks = [execute_autoupdate.apply_async((cron.id,)) for cron in crontabs]

    print(f"Dispatched {len(tasks)} tasks.")
    return {"dispatched_tasks": len(tasks)}


@app.task
def execute_autoupdate(cron_id):
    """
    Обработка одного cron.
    """
    print(f"Processing cron job ID: {cron_id}")
    # Здесь вы можете реализовать дополнительную логику обработки
    return {"cron_id": cron_id, "status": "success"}


@contextlib.asynccontextmanager
async def get_db_session():
    """
    Контекстный менеджер для управления сессией базы данных.
    """
    try:
        session = AsyncSessionLocal()
        yield session
    finally:
        await session.close()
        await engine.dispose()






