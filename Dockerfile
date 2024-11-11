# Используйте официальный образ Python
FROM python:3.10

# Установите рабочую директорию в контейнере
WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Скопируйте файлы зависимостей и установите их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте остальные файлы вашего приложения в контейнер
COPY . .

# Определите команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]