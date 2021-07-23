from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Prints
# Register your models here.

class PrintsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    save_on_top = True

admin.site.register(Prints, PrintsAdmin)
admin.site.site_title = 'Управение формами'
admin.site.site_header = 'Управение формами'
