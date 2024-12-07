from django.urls import path

from .views import Create, Enter, Inventory, PriceOzon, PriceWb, PriceYandex, FinanceOzon, PostavkaOzon, FinanceWb, Autoupdate, AutoupdateSettings

urlpatterns = [
    path('create/', Create.as_view(), name='create'),
    path('inventory/', Inventory.as_view(), name='inventory'),
    path('autoupdate/', Autoupdate.as_view(), name='autoupdate'),
    path('autoupdate_settings/', AutoupdateSettings.as_view(), name='autoupdate_settings'),
    path('price_ozon/', PriceOzon.as_view(), name='price_ozon'),
    path('finance_ozon/', FinanceOzon.as_view(), name='finance_ozon'),
    path('postavka_ozon/', PostavkaOzon.as_view(), name='postavka_ozon'),
    path('price_wb/', PriceWb.as_view(), name='price_wb'),
    path('finance_wb/', FinanceWb.as_view(), name='finance_wb'),
    path('price_yandex/', PriceYandex.as_view(), name='price_yandex'),
    path('', Enter.as_view(), name='enter'),
]



