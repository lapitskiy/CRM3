Установка plugin
-
plugin это приложение для установки с репозитория RepositoryCRM3 через REST api

plugin/settings_plugin.py
-
- содержит настройки для всех установленных плагинов и отсюда они добавляются в официальные django файлы. 

REPO_URL ссылка на текущий рабочий json репозиторий плагинов

INSTALLED_APPS_ADD перечень занчений для INSTALLED_APPS. Они добавляются в settings.py файле django INSTALLED_APPS += settings_plugin.INSTALLED_APPS_ADD

PLUGIN_URLS - пути плагинов приложений,которые добавляются в urls.py 

PLUGIN_CFG - настройки плагинов, для навигации и видежетов

plugin/templatetags/install_tags.py
-
содержит логику добавления плагина
- добавление плагина к глобальным настройкам, копирование файлов, миграции в базу данных, тесты

Удаление plugin
-
Удаление плагинов - в базе, и в конфигурационных файлах django