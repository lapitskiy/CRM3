from .models import Plugins
import importlib
from django.core.exceptions import ObjectDoesNotExist

class RelatedMixin(object):
    related_module_name = ''

    # list related apps

    def checkRelated(self):
        related = Plugins.objects.get(module_name=self.related_module_name)
        return related.related.all()

    # return related data from class get_related_data() in app models
    def getDataListRelated(self, **kwargs):
        data_related_list = []
        related = self.checkRelated()
        if related:
            for x in related:
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                for r in kwargs['page']:
                    try:
                        cls2 = cls.objects.get(related_uuid=r.related_uuid)
                        related_get = cls2.get_related_data()
                        # print('related_get', related_get)
                        data_related_list.append(related_get)
                    except ObjectDoesNotExist:
                        pass
        return data_related_list

    # return uuid related list for search query
    def getUuidListFilterRelated(self, search_query):
        uudi_filter_related_list = []
        related = self.checkRelated()
        if related:
            for x in related:
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                related_result = cls().get_related_filter(search_query=search_query)
                if related_result:
                    for z in related_result:
                        uudi_filter_related_list.append(z.related_uuid)
        return uudi_filter_related_list