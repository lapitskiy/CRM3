from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Задаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm3.settings')

app = Celery('crm3')

# Задаем настройки Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружаем задачи из зарегистрированных приложений
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')