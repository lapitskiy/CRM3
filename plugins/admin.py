from django.contrib import admin

from .models import Plugins

# Register your models here.

class PluginsAdmin(admin.ModelAdmin):

    list_display = ('id','title','version','is_active')
    list_display_links = ('id','title')
    search_fields = ('title','description')
    list_filter = ('is_active',)

    #def save_model(self, request, obj, form, change):
    #    obj.imp_name = 'test123'
    #    super(PluginsAdmin, self).save_model(request, obj, form, change)

admin.site.register(Plugins, PluginsAdmin)
