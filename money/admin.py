from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Money
# Register your models here.

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id','money','prepayment','created_at','updated_at','related_uuid')
    list_display_links = ('id',)
    list_editable = ('money', 'prepayment')
    search_fields = ('money','created_at')
    list_filter = ('money','created_at')
    fields = ('money','prepayment', 'created_at', 'updated_at')
    #readonly_fields = ('created_at', 'updated_at')
    save_on_top = True


admin.site.register(Money, MoneyAdmin)
admin.site.site_title = 'Управение деньгами'
admin.site.site_header = 'Управение деньгами'

