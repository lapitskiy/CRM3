from django.urls import path

from .views import Enter, Inventory, PriceOzon, PriceWb, PriceYandex, FinanceOzon, PostavkaOzon, FinanceWb, Autoupdate, AutoupdateSettings, OtpravlenieOzon, SettingsApi, \
    SettingsContragent

urlpatterns = [
    path('settings_api/', SettingsApi.as_view(), name='settings_api'),
    path('settings_contragent/', SettingsContragent.as_view(), name='settings_contragent'),
    path('inventory/', Inventory.as_view(), name='inventory'),
    path('autoupdate/', Autoupdate.as_view(), name='autoupdate'),
    path('', AutoupdateSettings.as_view(), name='autoupdate_settings'),
    path('price_ozon/', PriceOzon.as_view(), name='price_ozon'),
    path('finance_ozon/', FinanceOzon.as_view(), name='finance_ozon'),
    path('postavka_ozon/', PostavkaOzon.as_view(), name='postavka_ozon'),
    path('otpravlenie_ozon/', OtpravlenieOzon.as_view(), name='otpravlenie_ozon'),
    path('price_wb/', PriceWb.as_view(), name='price_wb'),
    path('finance_wb/', FinanceWb.as_view(), name='finance_wb'),
    path('price_yandex/', PriceYandex.as_view(), name='price_yandex'),
    path('enter/', Enter.as_view(), name='enter'),
]



