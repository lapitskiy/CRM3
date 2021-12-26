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

    # [RU] переводить dict uuid = {'uuid', ''} в _list = ['uuid',]
    # [RU] переводить list dict uuid = [{'uuid', ''},] в _list = ['uuid',]
    # [RU] бывший getListUuidFromDictKeyRelated
    # [EN] list related apps
    def dictUuidToList(self, uuid):
        #print('======')
        #print('uuid ', type(uuid))
        _list = []
        if type(uuid) == dict:
            for k, v in uuid.items():
                _list.append(k)
        if type(uuid) == list:
            for x in uuid:
                #print('x ', x)
                for k, v in x.items():
                    #print('k ', k)
                    _list.append(k)
        #if type(uuid) == django.db.models.query.QuerySet:
        #    print('zzzz')
        #print('_list ', _list)
        return _list

    # [EN] return related data from class get_related_data() in app models
    # [RU] возвращает связанные данные на основе выборки qry или page
    # 1) kwargs['page'] - возвращает связанные данные на основе полученного paginate page query
    def getDataListRelated(self, **kwargs):
        data_related_list = []
        related = self.checkRelated()
        #print('related ', related)
        if 'page' in kwargs:
            qry = kwargs['page']

        if related:
            for x in related:
                print('======= ')
                modelPath = x.module_name + '.models'
                imp_model = importlib.import_module(modelPath)
                cls_model = getattr(imp_model, x.related_class_name)
                relatedPath = x.module_name + '.related'
                imp_related = importlib.import_module(relatedPath)
                cls_related = getattr(imp_related, 'AppRelated')
                if 'one' in kwargs:
                    if kwargs['one'] == 'uuid':
                        try:
                            cls2 = cls_model.objects.get(Q(related_uuid__icontains=kwargs['uuid']))
                        except cls_model.DoesNotExist:
                            return ''
                        related_get = {}
                        if 'data' in kwargs:
                            if kwargs['data'] == 'full':
                                related_get[x.module_name] = cls2.__dict__
                                print('dict tyt zz')
                        else:
                            related_get = cls2.get_related_data()

                        related_get['related_uuid'] = kwargs['uuid']
                        data_related_list.append(related_get)
                else:
                    for r in qry:
                        for key_uuid, value_uuid in r.related_uuid.items():
                            try:
                                # доедлать, с класса related.py, вставить проверку на if и отдавать связаные данные для menu
                                if cls_related.related_format == 'data':
                                    cls2 = cls_model.objects.get(Q(related_uuid__icontains=key_uuid))
                                    related_get = cls2.get_related_data()
                                    related_get['related_uuid'] = key_uuid
                                    data_related_list.append(related_get)
                                if cls_related.related_format == 'menu':
                                    print('cls_model ', cls_model)
                                    cls_related2 = cls_model()
                                    related_get = cls_related2.get_related_data
                                    related_get['related_uuid'] = key_uuid
                                    print('related_get ', str(related_get))
                                    data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
        print('======= ')
        return data_related_list

    # [EN] return obj
    # [RU] возвращает объект на основе строк класса и app
    def getModelFromStr(self, **kwargs):
        if 'cls' in kwargs and 'app' in kwargs and 'uuid' in kwargs:
            modelPath = kwargs['app'] + '.models'
            imp_model = importlib.import_module(modelPath)
            cls_model = getattr(imp_model, kwargs['cls'])
            try:
                cls2 = cls_model.objects.get(Q(related_uuid__icontains=kwargs['uuid']))
                return cls2
            except cls_model.DoesNotExist:  # тоже самое с cls2.DoesNotExist:
                return False
        return False

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
        return self.dictUuidToList(uudi_filter_related_list)


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
                _dict= dict()
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()

                print('=================')
                if relatedClass.passEditUpdate():
                    continue

                _dict['module'] = x.module_name
                _dict['update'] = relatedClass.checkUpdate(request_post=request_post)

                if 'uuid' in kwargs:
                    _dict['convert'] = relatedClass.checkConvert(uuid=self.dictUuidToList(kwargs['uuid']),
                                                             request_post=request_post)
                    if 'edit' in kwargs['doing']:
                        _dict2 = relatedClass.checkRelatedEditForm(request_post=request_post, uuid=self.dictUuidToList(kwargs['uuid']))
                if 'add' in kwargs['doing']:
                    _dict2 = relatedClass.checkRelatedAddForm(request_post=request_post)
                _dict['uuid'] = _dict2['uuid']
                _dict['pk'] = _dict2['pk']
                _dict['form'] = _dict2['form']
                if _dict['form'].is_valid():
                    _dict['valid'] = True
                else:
                    _dict['valid'] = False
                related_form_dict[x.module_name] = _dict
        return related_form_dict


    # [RU] отдает ссылку для import submenu для формирования правильного submenu
    def relatedImportSubmenu(self, **kwargs):
        related = self.checkRelated()
        related_form_dict = {}
        if related:
            for x in related:
                _dict= {}
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                _dict['module'] = x.module_name
                print('rmodule ', x.module_name)
                _dict['submenu_import'] = relatedClass.submenuImportRelated()
                if _dict['submenu_import'] is not None:
                    related_form_dict[x.module_name] = _dict
        return related_form_dict

    # [RU] получает relateddata передаваемое в get запросе приложения и
    # [RU] обрабатывает его в соотвествии с правилами плагина и отдает список
    def relatedPostGetData(self, **kwargs):
        request_get = kwargs['request_get']
        related_dict = {}
        if request_get['relateddata']:
            related = self.checkRelated()
            if related:
                for x in related:
                    _dict= {}
                    imp_related = importlib.import_module(x.module_name + '.related')
                    getrelatedClass = getattr(imp_related, 'AppRelated')
                    relatedClass = getrelatedClass()
                    _dict['module'] = x.module_name

                    _dict['relateddata'] = self.dictUuidToList(relatedClass.linkGetReleatedData(request_get=request_get))
                    related_dict[x.module_name] = _dict
                return related_dict
        return related_dict

    # [RU] отдает dict с названием связанных плагинов и списком его доступных полей для вывода
    # [RU] пример работы плагина, это вывод перменных для вывода в печатных формах плагина prints
    def relatedGetAllFieldsFromModel(self, **kwargs):
        related_dict = {}
        related = self.checkRelated()
        if related:
            for x in related:
                _dict= {}
                _list= []
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                Cls = getattr(app_model, x.related_class_name)
                _dict['module'] = x.module_name

                for field in Cls._meta.__dict__.get('fields'):
                    _list.append(field.__str__())
                _dict['fields'] = _list
                related_dict[x.module_name] = _dict
            return related_dict
        return related_dict