from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Orders, Status, Category, Related, Service
# Register your models here.

class OrdersAdmin(admin.ModelAdmin):

    list_display = ('id','device','serial','created_at','updated_at','status')
    list_display_links = ('id','device')
    search_fields = ('device','serial')
    list_editable = ('status',)
    list_filter = ('status',)
    fields = ('device', 'serial', 'status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

class RelatedAdmin(admin.ModelAdmin):
    list_display = ('id','plugin')
    list_display_links = ('id','plugin')
    search_fields = ('plugin',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Related, RelatedAdmin)
admin.site.site_title = 'Управение заказами'
admin.site.site_header = 'Управение заказами'
