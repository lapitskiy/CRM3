from django.contrib import admin

from .models import Goods
# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id','goods')
    list_display_links = ('id',)
    list_editable = ('goods',)
    search_fields = ('goods',)
    list_filter = ('goods',)
    fields = ('goods',)
    save_on_top = True

admin.site.register(Goods, GoodsAdmin)
admin.site.site_title = 'Управение товарами'
admin.site.site_header = 'Управение товарами'