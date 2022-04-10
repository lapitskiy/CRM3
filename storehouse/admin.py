from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Storehouses
from .models import StoreRelated
# Register your models here.

class StorehousesAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone','category','related_user')
    list_display_links = ('name',)
    list_editable = ('address','phone')
    fields = ('name','address','phone')
    save_on_top = True

class StoreRelatedAdmin(admin.ModelAdmin):
    list_display = ('store','related_uuid')
    list_display_links = ('store',)
    save_on_top = True


admin.site.register(Storehouses, StorehousesAdmin)
admin.site.register(StoreRelated, StoreRelatedAdmin)
admin.site.site_title = 'Управение отделениями'
admin.site.site_header = 'Управение отделениями'