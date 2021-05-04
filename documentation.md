:twisted_rightwards_arrows: Bootstrap, rest api, django, mysql

Установка plugin
-
- plugin это приложение для установки с репозитория RepositoryCRM3 через REST api. Только приложение plugin является частью базовой установки CRM3, остальные приложения ставятся с репозитория
- приложение устанавливается, как обычный app django, после происходит автоматическая миграция данных и обновление файлов конфигурации

plugin/settings_plugin.py
-

- содержит настройки для всех установленных плагинов и отсюда они добавляются в официальные django файлы. 

REPO_URL ссылка на текущий рабочий json репозиторий плагинов

INSTALLED_APPS_ADD перечень значений для INSTALLED_APPS. Они добавляются в settings.py файле django INSTALLED_APPS += settings_plugin.INSTALLED_APPS_ADD
_INSTALLED_APPS_ADD = ['plugins.apps.PluginsConfig', 'pluginName.apps.pluginNameConfig']_

PLUGIN_URLS - пути плагинов приложений,которые добавляются в urls.py
_PLUGIN_URLS = {'pluginName': {'path': 'pluginName/', 'include': 'pluginName.urls'}}_ 

PLUGIN_CFG - настройки плагинов, для навигации и видежетов
_PLUGIN_CFG = {'pluginName': {'nav_url': 'pluginName_home', 'nav_name': 'Name in menu'}}_

plugin/templatetags/install_tags.py
-
содержит логику добавления плагина
- добавление плагина к глобальным настройкам, копирование файлов, миграции в базу данных, тесты

Удаление plugin
-
Удаление плагинов - в базе, и в конфигурационных файлах django

Создание плагина
-
pluginName/template/include/_sidebar_orders.html 
рекомендованый файл сайдбара

pluginName/template/pluginName/sidebar_orders_tags.html 
рекомендованый файл tag.html

pluginName/templatetags//sidebar_orders_tags.py 
рекомендованый файл tag.py

install.py - обязательный файл с настройками приложения

def get_related_data() - связанные данные которые отдает приложение

def get_related_filter() - фильтр для связаннных данных со своей логикой

Настройки плагина в файле install.py
-
данные для установки плагина

MODULE_NAME = 'pluginName'

INSTALLED_APPS_NAME = 'pluginName.apps.OrderConfig'

PLUGIN_CFG_UPDATE = {
    'pluginName': {
        'nav_url': 'pluginName_home',
        'nav_name': 'Имя в меню'}}

INSTALLED_URL = {
    'pluginName': {
        'path': 'pluginName/',
        'include': 'pluginName.urls'}}
        
Установка демо данных плагина
def demodata в файле install.py
      


related
-
- приложения связываются в настройках приложения
- если приложение активно, оно автоматически добавляется в верхнее меню
- база каждого приложения(плагина) для создания связанных данных с другими приложениями в модели plugins есть переменная related_uuid, которая связывает данные между любыми приложениями
- пример вывода связанных данных в виде форм или данных можно посмотреть в файле views приложения orders
- relatedMixin (plugins.utils) класс с методами для вызова связанных данных, который использует общую логику для всех приложений. Получение связанных данных и обработка, вывод связанного меню (пример в приложении money)


install.py
-



        