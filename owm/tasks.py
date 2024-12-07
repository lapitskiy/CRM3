from .models import Crontab

from crm3.celery import app

@app.task
def sync_inventory_owm():
    crontab = Crontab.objects.filter(name='autoupdate', active=True)  # Замените `.all()` фильтром, если необходимо

    for cron in crontab:
        # Проверяем булевое поле, например, 'is_active'
        if cron.active:  # Замените 'is_active' на название вашего поля
            print(f"Cron task")  # Замените 'name' на поле, содержащее имя пользователя

        else:
            print(f"No cron task")

    return "Task completed"