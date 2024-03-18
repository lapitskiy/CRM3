from .models import Plugins, DesignRelatedPlugin
import importlib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import logging
import time

#logging.basicConfig(level='DEBUG')
logger = logging.getLogger('crm3_error')#('crm3_info')


class RelatedMixin(object):
    related_module_name = ''

    def checkRelated(self) -> object:
        """Проверка связанных данных

        Функция возвращает все связанные приложения с указанным приложеним в переменной related_module_name.
        Возвращется ввиде обьекта related = Plugins.objects.get(module_name=self.related_module_name)
        то есть список из модели manytomany, который потом обычным перебором проверять.
        Пример в приложении orders в views

        :rtype: object get
        """
        try:
            related = Plugins.objects.get(module_name=self.related_module_name)
            return related.related.all()
        except Plugins.DoesNotExist:
            if self.related_module_name == '':
                logger.error('csl checkRelated. Не указан related_module_name')
            else:
                logger.error('csl checkRelated. Приложение не установлено. Записи нет в базе данных.')

    def relatedFormat(self) -> object:
        """
        Позиции дизайна

        :rtype: object filter
        """
        print(f"position")
        try:
            position = DesignRelatedPlugin.objects.filter(related_many_plugin__module_name=self.related_module_name)
            print(f"position {position.values()}")
            return position
        except DesignRelatedPlugin.DoesNotExist:
            if self.related_module_name == '':
                logger.error('csl checkRelated. Не указан related_module_name')
            else:
                logger.error('DesignRelatedPlugin. Приложение не установлено. Записи нет в базе данных.')

    # [RU] возвращает все связанные формы
    # [EN] list related forms
    def getRelatedFormList(self, **kwargs):
        related = self.checkRelated()
        form_list = []
        if related:
            for x in related:
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                if relatedClass.passAddUpdate():
                    continue
                formPath = x.module_name + '.forms'
                app_form = importlib.import_module(formPath)
                related_form = app_form.RelatedAddForm(request=kwargs['request'])
                related_form.prefix = x.module_name
                form_list.append(related_form)
        return form_list

    # [RU] проверяет связанные данные и выдает финальный чистый queryset. тоесть удаляет записи которые не должны
    # [RU] показываться конкретному пользователю или по опредленным параметрам указанных в каждом приложнении.
    # [EN] wait translate
    def getCleanQueryset(self, **kwargs):
        related = self.checkRelated()  # --- 0.005012989044189453 seconds ---
        queryset = kwargs['queryset']
        if related:
            for x in related:
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                if relatedClass.passCleanQueryset():
                    continue
                #print('enter ', queryset)
                queryset = relatedClass.checkCleanQueryset(queryset=kwargs['queryset'], request=kwargs['request']) # --- 0.009974241256713867 seconds ---
                #print('exit ', queryset)

        #  --- 0.01399374008178711 seconds ---
        return queryset

    # [RU] возвращает все связанные формы для edit GET
    # [EN] list related forms
    def getRelatedEditFormList(self, **kwargs):
        start_time = time.time()
        related = self.checkRelated()
        form_list = []
        obj = kwargs['obj']
        #obj_uuid_list = obj.objects.values_list('uuid__related_uuid', flat=True)
        obj_uuid_list = obj.uuid.all().values_list('related_uuid', flat=True)
        if related:
            for x in related:
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                if relatedClass.passEditUpdate():
                    continue
                formPath = x.module_name + '.forms'
                modelPath = x.module_name + '.models'
                app_form = importlib.import_module(formPath)
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                #obj_uuid_list = list(filter(lambda a: a != None, obj_uuid_list))
                #obj_uuid_list = list(filter((None).__ne__, obj_uuid_list))
                for uuid in obj_uuid_list:
                    try:
                        get_related = cls.objects.get(uuid__related_uuid=uuid)
                        related_form = app_form.RelatedAddForm(instance=get_related)
                    except cls.DoesNotExist:
                        related_form = app_form.RelatedAddForm()
                related_form.prefix = x.module_name
                form_list.append(related_form)
        print(" --- %s seconds getRelatedEditFormList ---" % (time.time() - start_time))
        return form_list

    # [RU] переводить dict uuid = {'uuid', ''} в _list = ['uuid',]
    # [RU] переводить list dict uuid = [{'uuid', ''},] в _list = ['uuid',]
    # [RU] бывший getListUuidFromDictKeyRelated
    # [EN] list related apps
    '''
    def dictUuidToList(self, uuid) -> list:
        _list = []
        if type(uuid) == dict:
            for k, v in uuid.items():
                _list.append(k)
        if type(uuid) == list:
            #print('=================================')
            #print('dictUuidToList uuid ', uuid)

            for x in uuid:
                if type(x) == tuple or type(x) == list:
                    x = x[0]
                if isinstance(x, dict):
                    for k, v in x.items():
                        _list.append(k)
        return _list
    '''

    # [EN] return related data from class get_related_data() in app models
    # [RU] возвращает связанные данные на основе выборки qry или page
    # 1) kwargs['page'] - возвращает связанные данные на основе полученного paginate page query
    # query_paginator_page - метод для работы с query после функции paginator
    def getDataListRelated(self, **kwargs) -> list:
        data_related_list = []
        related = self.checkRelated() # obj get
        format = self.relatedFormat() # obj filter
        if kwargs['method'] == 'query_paginator_page':
            #print('tyt', qry.object_list.)
            if 'qry_uuid_list' in kwargs:
                qry_uuid_list = kwargs['qry_uuid_list']
                print('qry_uuid_list ', qry_uuid_list)
            else:
                qry = kwargs['query']
                qry_uuid_list = list(qry.object_list.values_list('uuid__related_uuid', flat=True))
            # q = q.value_list('uuid')
        if kwargs['method'] == 'get_one_obj_by_qry':
            if 'qry_uuid_list' in kwargs:
                qry_uuid_list = kwargs['qry_uuid_list']
                print('qry_uuid_list ', qry_uuid_list)
            else:
                qry = kwargs['query']
                qry_uuid_list = list(qry.values_list('uuid__related_uuid', flat=True))
            # q = q.value_list('uuid')

        if related:
            for x in related:
                #print('======= utils.py getDataListRelated')
                modelPath = x.module_name + '.models'
                imp_model = importlib.import_module(modelPath)
                cls_model = getattr(imp_model, x.related_class_name)
                relatedPath = x.module_name + '.related'
                imp_related = importlib.import_module(relatedPath)
                cls_related = getattr(imp_related, 'AppRelated')

                if kwargs['method'] == 'get_one_obj_by_str_uuid':
                    related_get = {}
                    if 'data' in kwargs:
                        if kwargs['data'] == 'dict':
                            obj = cls_model.get_related_by_uuid(uuid=kwargs['uuid'])
                            related_get[x.module_name] = obj.get_related_dict_data()
                    related_get['uuid'] = kwargs['uuid']
                    print(x.module_name, ': ', related_get)
                    print('=================')
                    data_related_list.append(related_get)
                if kwargs['method'] == 'get_one_obj_by_qry':
                    if cls_related.related_data_format == 'form':
                        for uuid in qry_uuid_list:
                            try:
                                #print('uuid money ', qry_uuid_list)
                                r_cls = cls_model.objects.get(uuid__related_uuid=uuid)
                                related_get = r_cls.get_related_data()
                                related_get['uuid'] = uuid
                                data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
                    if cls_related.related_data_format == 'link':
                        r_cls = cls_model()
                        related_get = r_cls.get_related_data(related_uuid=uuid)
                        related_get['uuid'] = uuid
                        data_related_list.append(related_get)
                    if cls_related.related_data_format == 'text':
                        for uuid in qry_uuid_list:
                            try:
                                r_cls = cls_model.objects.get(uuid__related_uuid=uuid)
                                related_get = r_cls.get_related_data()
                                related_get['uuid'] = uuid
                                data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
                if kwargs['method'] == 'query_paginator_page':
                    print('====================')
                    print('module_name: ', cls_related.related_module_name)

                    if cls_related.related_format == 'form':
                        for uuid in qry_uuid_list:
                            try:
                                cls2 = cls_model.objects.get(uuid__related_uuid=uuid)
                                related_get = cls2.get_related_data()
                                related_get['uuid'] = uuid
                                data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
                    if format:
                        for k in format:
                            if k.related_plugin == x:
                                all_format = k.related_format.all()
                            if k.related_plugin == x:
                                for z in all_format:
                                    if z.format == 'link':
                                        for uuid in qry_uuid_list:
                                            cls_related2 = cls_model()
                                            related_get = cls_related2.get_related_data(related_uuid=uuid)
                                            related_get['uuid'] = uuid
                                            data_related_list.append(related_get)

                    if cls_related.related_format == 'select':
                        logger.info('cls_model select utils %s', cls_model)
                        for uuid in qry_uuid_list:
                            try:
                                cls2 = cls_model.objects.get(uuid__related_uuid=uuid)
                                related_get = cls2.get_related_data()
                                related_get['uuid'] = uuid
                                data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
        #print('======= data_related_list')
        #print(data_related_list)
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
                #print('####START ')
                #print('related_result ',x.module_name,' :',related_result)
                #print('####END')
                if related_result:
                    for z in related_result:
                        all_uuid = list(z.uuid.all().values_list('related_uuid', flat=True))
                        for u in all_uuid:
                            uudi_filter_related_list.append(u)
        return uudi_filter_related_list

    '''
    # return uuid related list for search query
    def relatedDeleteMultipleUuid(self, **kwargs):
        if 'dictt' in kwargs:
            dictt = kwargs['dictt']
            #print('dictt', dictt)
            dictt['deleteuuid'] = kwargs['deleteUuid']
            #imp_related = importlib.import_module(dictt['module'] + '.related')
            #getrelatedClass = getattr(imp_related, 'AppRelated')
            #relatedClass = getrelatedClass()
            relatedClass = dictt['class']
            relatedClass.deleteRelatedMultipleUuid(dictt=dictt)

    '''
    # [RU] отдает dict c формой переданного post для add или edit form, валидация, uuid, данные update
    # ? исползуется в выводе связанных моделуй
    # ? dict['update'] - может ли данный модуль иметь возможность создерать несколько uuid. Например один телефон для многих заказов. Возвращате true false
    # ? how - sting -  add or edit parametr
    def checkRelatedFormDict(self, request_post, **kwargs):
        related = self.checkRelated()
        related_form_dict = {}
        if 'uuid' in kwargs:
            uuid = list(kwargs['uuid'].values_list('related_uuid', flat=True))
        if related:
            for x in related:
                _dict= dict()
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()

                print('=================')
                if 'add' in kwargs['method'] and relatedClass.passAddUpdate():
                    continue
                if 'edit' in kwargs['method'] and relatedClass.passEditUpdate():
                    continue

                #_dict['module'] = x.module_name
                #_dict['update'] = relatedClass.checkUpdate(request_post=request_post)

                if 'uuid' in kwargs:
                    if kwargs['method'] == 'edit':
                        _dict2 = relatedClass.checkRelatedEditForm(request_post=request_post, uuid=uuid)
                if 'add' in kwargs['method']:
                    _dict2 = relatedClass.checkRelatedAddForm(request_post=request_post, request=kwargs['request'])
                    #print('!self.request ', self.request)


                _dict['uuid'] = _dict2['uuid']
                _dict['pk'] = _dict2['pk']
                _dict['form'] = _dict2['form']
                _dict['class'] = relatedClass
                _dict['valid'] = _dict2['valid']
                related_form_dict[x.module_name] = _dict

        # если хотя бы в одной форме нет валида, отдаем переменную is_valid_dict=False
        is_valid_dict = {}
        is_valid_dict['is_valid'] = True
        form_list = []
        for k, v in related_form_dict.items():
            if not v['valid']: is_valid_dict['is_valid'] = False
            form_list.append(v['form'])
        is_valid_dict['form'] = form_list
        return related_form_dict, is_valid_dict

    # [RU] получает dict из checkRelatedFormDict для сохранения формы в модель, после проверки валидности на этапе checkRelatedFormDict
    def saveRelatedFormData(self, request, **kwargs):
        related_form_dict = kwargs['related_form_dict']
        related_uuid = kwargs['related_uuid']
        #print('related_form_dict', related_form_dict)
        for k, v in related_form_dict.items():
            #if related_form_dict[k]['update']:
            #    update_uuid_dict = related_uuid
            #    update_uuid_dict.update(related_uuid)
            #    related_form_dict[k]['uuid'] = update_uuid_dict
            #else:
            #    related_form_dict[k]['uuid'] = related_uuid
            related_form_dict[k]['uuid'] = related_uuid
            relatedClass = related_form_dict[k]['class']
            relatedClass.saveForm(related_form_dict=related_form_dict[k], request=request, method=kwargs['method'])
        return


    # [RU] отдает ссылку для import submenu для формирования правильного submenu
    def relatedImportSubmenu(self, **kwargs):
        # if 'request' in kwargs:
        #     request = kwargs['request']
        # else:
        #     request = None
        related = self.checkRelated()
        related_form_dict = {}
        if related:
            for x in related:
                _dict= {}
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                _dict['module'] = x.module_name
                _dict['submenu_import'] = relatedClass.submenuImportRelated()
                #print('submenu_import ', _dict['submenu_import'])
                if _dict['submenu_import'] is not None:
                    related_form_dict[x.module_name] = _dict
        return related_form_dict

    # [RU] получает relateddata передаваемое в get запросе приложения и
    # [RU] обрабатывает его в соотвествии с правилами плагина и отдает список
    def relatedPostGetData(self, **kwargs):
        request_get = kwargs['request_get']

        related_dict = {}
        logger.info('%s relatedPostGetData ', __name__)
        if 'rdata_' in str(request_get):
            related = self.checkRelated()
            logger.info('%s related: %s', __name__, related)
            if related:
                for x in related:
                    _dict= {}
                    imp_related = importlib.import_module(x.module_name + '.related')
                    getrelatedClass = getattr(imp_related, 'AppRelated')
                    relatedClass = getrelatedClass()
                    _dict['module'] = x.module_name
                    #print('relatedPostGetData module ', x.module_name)
                    _dict['relateddata'] = relatedClass.linkGetReleatedData(request_get=request_get)
                    related_dict[x.module_name] = _dict
                return related_dict
        return related_dict

    # [RU] отдает dict с названием связанных плагинов и списком его доступных полей для вывода
    # [RU] пример работы плагина, это вывод перменных для вывода в печатных формах плагина prints
    def relatedGetAllFieldsFromModel(self, **kwargs) -> dict:
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
            print('related_dict', related_dict)
            return related_dict
        return related_dict