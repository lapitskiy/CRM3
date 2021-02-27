from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Clients, Related
# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','created_at','updated_at')
    list_display_links = ('id','name')
    search_fields = ('name','phone')
    list_editable = ('phone',)
    list_filter = ('phone',)
    fields = ('name', 'phone', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True

class RelatedAdmin(admin.ModelAdmin):
    list_display = ('id','plugin')
    list_display_links = ('id','plugin')
    search_fields = ('plugin',)

admin.site.register(Clients, ClientsAdmin)
admin.site.register(Related, RelatedAdmin)
admin.site.site_title = 'Управение клиентами'
admin.site.site_header = 'Управение клиентами'
