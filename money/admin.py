from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Money, Prepayment
# Register your models here.

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id','money','created_at','related_uuid')
    list_display_links = ('id',)
    list_editable = ('money',)
    search_fields = ('money','created_at')
    list_filter = ('money','created_at')
    fields = ('money', 'created_at')
    save_on_top = True

class PrepaymentAdmin(admin.ModelAdmin):
    list_display = ('id','prepayment','comment','created_at')
    list_display_links = ('id','prepayment')


admin.site.register(Money, MoneyAdmin)
admin.site.register(Prepayment, PrepaymentAdmin)
admin.site.site_title = 'Управение деньгами'
admin.site.site_header = 'Управение деньгами'

