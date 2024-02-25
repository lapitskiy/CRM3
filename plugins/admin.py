from django.contrib import admin

from .models import Plugins, PluginsCategory, RelatedFormat

# Register your models here.

class PluginsAdmin(admin.ModelAdmin):

    list_display = ('id','title','version','is_active')
    list_display_links = ('id','title')
    search_fields = ('title','description')
    list_filter = ('is_active',)

    #def save_model(self, request, obj, form, change):
    #    obj.imp_name = 'test123'
    #    super(PluginsAdmin, self).save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

class PluginsRelatedAdmin(admin.ModelAdmin):
    list_display = ('id',)

class RelatedFormatAdmin(admin.ModelAdmin):

    list_display = ('id','format')
    list_display_links = ('id','format')

admin.site.site_title = 'Управение plugin'
admin.site.site_header = 'Управение plugin'

admin.site.register(Plugins, PluginsAdmin)
admin.site.register(PluginsCategory, CategoryAdmin)
admin.site.register(RelatedFormat, RelatedFormatAdmin)
