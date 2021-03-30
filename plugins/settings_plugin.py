# CRM3 GLOBAL PLUGINS VARS
REPO_URL = 'http://127.0.0.1:8001/plugins/api/?format=json'
INSTALLED_APPS_ADD = ['orders.apps.OrderConfig', 'clients.apps.ClientConfig', 'money.apps.MoneyConfig']
PLUGIN_URLS = {'orders': {'path': 'orders/', 'include': 'orders.urls'}, 'clients': {'path': 'clients/', 'include': 'clients.urls'}, 'money': {'path': 'money/', 'include': 'money.urls'}}
PLUGIN_CFG = {'orders': {'nav_url': 'orders_home', 'nav_name': 'Заказы'}, 'clients': {'nav_url': 'clients_home', 'nav_name': 'Клиенты'}, 'money': {'nav_url': 'money_home', 'nav_name': 'Бухгалтерия'}}