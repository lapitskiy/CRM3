# CRM3 GLOBAL PLUGINS VARS
REPO_URL = 'http://127.0.0.1:8001/plugins/api/?format=json'
INSTALLED_APPS_ADD = ['plugins.apps.PluginsConfig', 'orders.apps.OrderConfig']
PLUGIN_URLS = {'orders': {'path': 'orders/', 'include': 'orders.urls'}}
PLUGIN_CFG = {'orders': {'nav_url': 'orders_home', 'nav_name': 'Заказы'}}