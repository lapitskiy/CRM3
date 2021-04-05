from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Orders, Status, Category, Service
# Register your models here.

class OrdersAdmin(admin.ModelAdmin):

    list_display = ('id','device','serial','category','created_at','updated_at','status','related_uuid','related_user')
    list_display_links = ('id','device')
    search_fields = ('device','serial')
    list_editable = ('status',)
    list_filter = ('status',)
    fields = ('device', 'serial', 'status', 'category', 'created_at', 'updated_at')
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

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.site_title = 'Управение заказами'
admin.site.site_header = 'Управение заказами'
