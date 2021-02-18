from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Orders, Status
# Register your models here.

class OrdersAdmin(admin.ModelAdmin):

    list_display = ('id','gadget','serial','created_at','updated_at','status')
    list_display_links = ('id','gadget')
    search_fields = ('gadget','serial')
    list_editable = ('status',)
    list_filter = ('status',)
    fields = ('gadget', 'serial', 'status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.site_title = 'Управение заказами'
admin.site.site_header = 'Управение статусами'
