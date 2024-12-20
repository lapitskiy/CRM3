#!/bin/bash

# Запускаем Redis в демонизированном режиме
redis-server /usr/local/etc/redis/redis.conf --requirepass "Billkill13" --daemonize yes
sleep 1  # Небольшая пауза для инициализации Redis

# Выполняем очистку базы данных
redis-cli -a "Billkill13" FLUSHDB

# Останавливаем временный процесс Redis
redis-cli -a "Billkill13" shutdown

# Перезапускаем Redis в обычном режиме
redis-server /usr/local/etc/redis/redis.conf --requirepass "Billkill13"