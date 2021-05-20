from .models import Plugins
import importlib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

class RelatedMixin(object):
    related_module_name = ''

    # [RU] возвращает все связанные приложения
    # [EN] list related apps
    def checkRelated(self):
        related = Plugins.objects.get(module_name=self.related_module_name)
        return related.related.all()

    def dictUuidToList(self, uuid):
        _list = []
        for k, v in uuid.items():
            _list.append(k)
        return _list


    # [EN] return related data from class get_related_data() in app models
    # [RU] возвращает связанные данные
    # 1) kwargs['page'] - возвращает связанные данные на основе полученного paginate page query
    def getDataListRelated(self, **kwargs):
        data_related_list = []
        related = self.checkRelated()
        if related:
            for x in related:
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                for r in kwargs['page']:
                    for key_uuid, value_uuid in r.related_uuid.items():
                        try:
                            cls2 = cls.objects.get(Q(related_uuid__icontains=key_uuid))
                            related_get = cls2.get_related_data()
                            related_get['related_uuid'] = key_uuid
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

        result_list = [] # only key uuid from dict related_uuid
        for x in uudi_filter_related_list:
            for key, value in x:
                result_list.append(key)
        return result_list

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

        result_list = []  # only key uuid from dict related_uuid
        for x in uudi_filter_related_list:
            for key, value in x:
                result_list.append(key)
        return getListUuidFromDictKeyRelated()

    # return uuid related list for search query
    def getListUuidFromDictKeyRelated(self, related_uuid_dict):
        result_list = []  # only key uuid from dict related_uuid
        for x in related_uuid_dict:
            for key, value in x:
                result_list.append(key)
        return result_list

    # return uuid related list for search query
    def relatedDeleteMultipleUuid(self, **kwargs):
        if kwargs['dictt']:
            dictt = kwargs['dictt']
            dictt['deleteuuid'] = kwargs['deleteUuid']
            imp_related = importlib.import_module(dictt['module'] + '.related')
            getrelatedClass = getattr(imp_related, 'AppRelated')
            relatedClass = getrelatedClass()
            relatedClass.deleteRelatedMultipleUuid(dictt=dictt)

    # [RU] отдает dict c формой переданного post для add или edit form, валидация, uuid, данные update
    # ? исползуется в выводе связанных моделуй
    # ? dict['update'] - может ли данный модуль иметь возможность создерать несколько uuid. Например один телефон для многих заказов. Возвращате true false
    # ? how - sting -  add or edit parametr
    def checkRelatedIsValidDict(self, request_post, **kwargs):
        related = self.checkRelated()
        related_form_dict = {}
        if related:
            for x in related:
                _dict= {}
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                _dict['module'] = x.module_name
                _dict['update'] = relatedClass.checkUpdate(request_post=request_post)
                _dict['convert'] = relatedClass.checkConvert(uuid=self.dictUuidToList(kwargs['uuid']), request_post=request_post)
                if 'add' in kwargs['doing']:
                    _dict2 = relatedClass.checkRelatedAddForm(request_post=request_post)
                if 'edit' in kwargs['doing']:
                    _dict2 = relatedClass.checkRelatedEditForm(request_post=request_post, uuid=self.dictUuidToList(kwargs['uuid']))
                _dict['form'] = _dict2['form']
                _dict['uuid'] = _dict2['uuid']
                _dict['pk'] = _dict2['pk']
                if _dict['form'].is_valid():
                    _dict['valid'] = True
                else:
                    _dict['valid'] = False
                related_form_dict[x.module_name] = _dict
        return related_form_dict