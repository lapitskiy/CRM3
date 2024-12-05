from .models import Parser

from crm3.celery import app

@app.task
def my_periodic_task():
    print("This task runs every 10 minutes.")
    return "Task completed"

@app.task
def test_task():
    print("Beat task works!")
    return "Success"

'''
@shared_task
def sync_products():
    # Проходим по всем пользователям с флагом
    parsers = Parser.objects.filter(flag=True)
    for parser in parsers:
        # Здесь ваша логика работы с каждым пользователем
        result = add(2, 3)  # Или что-то более сложное
        print(f"Processed parser for user_id={parser.user_id}")
    return f"Processed {parsers.count()} parsers"
'''