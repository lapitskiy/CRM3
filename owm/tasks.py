from eventlet import monkey_patch
monkey_patch()

import asyncio

from .models import parser_table, crontab_table
from crm3.celery import app
from .utils import autoupdate_sync_inventory, autoupdate_get_last_sync_acquisition_writeoff_ms
from sqlalchemy.future import select
from crm3.utils_db import AsyncSessionLocal, engine, get_db_session
from asgiref.sync import async_to_sync
from sqlalchemy.sql import join
from sqlalchemy.schema import MetaData
import aiohttp


@app.task
def sync_inventory_owm():
    """
    Основная задача, которая диспетчеризует асинхронные задачи для всех активных cron.
    """
    #print('Starting sync_inventory_owm...')
    result = async_to_sync(run_sync_inventory)()  # Запуск корутины синхронно
    print('sync_inventory_owm completed.')
    #for item in result:
    #    process_row_data.delay(item)

    #return result

'''
@app.task(name="process_row_data")
def process_row_data(item):
    """
    Обработка данных одного cron.
    """
    print(f"autoupdate_sync_inventory success")
    #await autoupdate_get_last_sync_acquisition_writeoff_ms(headers=item['headers'], cron_data=item['cron_data'])
    async_to_sync(autoupdate_get_last_sync_acquisition_writeoff_ms)(headers=item[0]['headers'], cron_data=item[0]['cron_data'])
'''

#@app.task(name="run_sync_inventory", bind=True)
#async def run_sync_inventory(self):



async def run_sync_inventory():
    """
    Асинхронная обработка всех активных cron через SQLAlchemy.
    """
    #print('Fetching cron jobs...')

    async with get_db_session() as session:
        query = select(crontab_table).where(
            (crontab_table.c.name == "autoupdate") & (crontab_table.c.active == True)
        )
        result = await session.execute(query)
        crontabs = result.fetchall()

    for cron in crontabs:
        await run_autoupdate(cron.id)

    #row_list = []
    #for cron in crontabs:
    #    result = await run_autoupdate(cron.id)
    #    row_list.append(result)
    #return row_list

    #print(f"Dispatched {len(tasks)} tasks.")
    #return {"dispatched_tasks": len(tasks)}


async def run_autoupdate(cron_id):
    """
    Асинхронная обработка одного cron.
    """
    #print(f"Running autoupdate for cron ID: {cron_id}")
    #row_list = await autoupdate_sync_inventory(cron_id=cron_id)
    await autoupdate_sync_inventory(cron_id=cron_id)
    #return row_list

'''
@app.task
def execute_autoupdate(cron_id):
    """
    Обработка одного cron.
    """
    #print(f"Processing cron job ID: {cron_id}")
    async_to_sync(run_autoupdate)(cron_id)
    # Здесь вы можете реализовать дополнительную логику обработки
    #return {"cron_id": cron_id, "status": "success"}
'''







