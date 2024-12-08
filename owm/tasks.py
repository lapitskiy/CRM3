from .models import Crontab

from crm3.celery import app
from .utils import sync_inventory


@app.task
def sync_inventory_owm():
    crontab = Crontab.objects.filter(name='autoupdate', active=True)  # Замените `.all()` фильтром, если необходимо

    for cron in crontab:
        if cron.active:
            sync_inventory(obj=cron)
            print(f"Cron task")
        else:
            print(f"No cron task")

    return "Task completed"