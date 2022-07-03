from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Orders, Status, Category, Service, Device, Category_service
# Register your models here.

class OrdersAdmin(admin.ModelAdmin):

    list_display = ('id','device','serial','service','category','created_at','updated_at','status','related_uuid','related_user')
    list_display_links = ('id','device', 'service')
    search_fields = ('device','serial')
    list_editable = ('status',)
    list_filter = ('status','device','service')
    fields = ('service', 'device', 'serial', 'status', 'category', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category')
    list_display_links = ('id','title', 'category')
    search_fields = ('title',)

class CategoryServiceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category')
    list_display_links = ('id','name', 'category')
    search_fields = ('title',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('name',)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('name',)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Category_service, CategoryServiceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.site_title = 'Управение заказами'
admin.site.site_header = 'Управение заказами'
