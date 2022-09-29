from .models import Plugins
import importlib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import logging

#logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

class RelatedMixin(object):
    related_module_name = ''

    def checkRelated(self):
        """Проверка связанных данных

        Функция возвращает все связанные приложения с указанным приложеним в переменной related_module_name.
        Возвращется ввиде обьекта related = Plugins.objects.get(module_name=self.related_module_name)
        то есть список из модели manytomany, который потом обычным перебором проверять.
        Пример в приложении orders в views

        :rtype: object
        """
        related = Plugins.objects.get(module_name=self.related_module_name)
        return related.related.all()

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
        related = self.checkRelated()
        queryset = kwargs['queryset']
        if related:
            for x in related:
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()
                if relatedClass.passCleanQueryset():
                    continue
                queryset = relatedClass.checkCleanQueryset(queryset=kwargs['queryset'], request=kwargs['request'])
        return queryset

    # [RU] возвращает все связанные формы для edit GET
    # [EN] list related forms
    def getRelatedEditFormList(self, **kwargs):
        related = self.checkRelated()
        form_list = []
        obj = kwargs['obj']
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
                for key_uuid, value_uuid in obj.related_uuid.items():
                    try:
                        get_related = cls.objects.get(Q(related_uuid__icontains=key_uuid))
                        related_form = app_form.RelatedAddForm(instance=get_related)
                    except cls.DoesNotExist:
                        related_form = app_form.RelatedAddForm()
                related_form.prefix = x.module_name
                form_list.append(related_form)
        return form_list

    # [RU] переводить dict uuid = {'uuid', ''} в _list = ['uuid',]
    # [RU] переводить list dict uuid = [{'uuid', ''},] в _list = ['uuid',]
    # [RU] бывший getListUuidFromDictKeyRelated
    # [EN] list related apps
    def dictUuidToList(self, uuid):
        #print('======')
        #print('uuid ', type(uuid))
        _list = []
        #print('####################>>>>>>>>>>>>>')
        #print('uuid type ', type(uuid))
        if type(uuid) == dict:
            for k, v in uuid.items():
                _list.append(k)
        if type(uuid) == list:
            for x in uuid:
                if type(x) == tuple or type(x) == list:
                    x = x[0]
                    #print('', type(x))
                #print('[utils.py 33] type x: ', x, '; type: ', type(x))
                for k, v in x.items():

                    #print('k ', k)
                    _list.append(k)
        #if type(uuid) == django.db.models.query.QuerySet:
        #    print('zzzz')
        #print('_list ', _list)
        #print('####################<<<<<<<<<<<<<<')
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
                #print('======= utils.py getDataListRelated')
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
                        else:
                            related_get = cls2.get_related_data()

                        related_get['related_uuid'] = kwargs['uuid']
                        data_related_list.append(related_get)
                else:
                    for r in qry:
                        for key_uuid, value_uuid in r.related_uuid.items():
                            try:
                                # доедлать, с класса related.py, вставить проверку на if и отдавать связаные данные для menu
                                if cls_related.related_format == 'form':
                                    cls2 = cls_model.objects.get(Q(related_uuid__icontains=key_uuid))
                                    related_get = cls2.get_related_data()
                                    related_get['related_uuid'] = key_uuid
                                    data_related_list.append(related_get)
                                if cls_related.related_format == 'link':
                                    #print('cls_model link', cls_model)
                                    cls_related2 = cls_model()
                                    related_get = cls_related2.get_related_data
                                    related_get['related_uuid'] = key_uuid
                                    #print('related_get ', str(related_get))
                                    data_related_list.append(related_get)
                                if cls_related.related_format == 'select':
                                    logger.info('cls_model select utils', cls_model)
                                    cls_related3 = cls_model.objects.get(Q(related_uuid__icontains=key_uuid))
                                    related_get = cls_related3.get_related_data
                                    #print('tyt 333 ky uuid', key_uuid)
                                    #print('related_get select', str(related_get))
                                    related_get['related_uuid'] = key_uuid
                                    #print('related_get ', str(related_get))
                                    data_related_list.append(related_get)
                            except ObjectDoesNotExist:
                                pass
        #print('======= data_related_list')
        #print(data_related_list)
        return data_related_list

    # [EN] return obj
    # [RU] возвращает объект на основе строк класса и app
    def getModelFromStr(self, **kwargs):
        if 'cls' in kwargs and 'app' in kwargs and 'uuid' in kwargs:
            modelPath = kwargs['app'] + '.models'
            print('model path ', modelPath)
            imp_model = importlib.import_module(modelPath)
            print('NO!')
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
                print('####START ')
                print('related_result ',x.module_name,' :',related_result)
                print('####END')
                if related_result:
                    for z in related_result:
                        uudi_filter_related_list.append(z.related_uuid)
        return self.dictUuidToList(uudi_filter_related_list)


    # return uuid related list for search query
    def relatedDeleteMultipleUuid(self, **kwargs):
        if 'dictt' in kwargs:
            dictt = kwargs['dictt']
            print('dictt', dictt)
            dictt['deleteuuid'] = kwargs['deleteUuid']
            #imp_related = importlib.import_module(dictt['module'] + '.related')
            #getrelatedClass = getattr(imp_related, 'AppRelated')
            #relatedClass = getrelatedClass()
            relatedClass = dictt['class']
            relatedClass.deleteRelatedMultipleUuid(dictt=dictt)


    # [RU] отдает dict c формой переданного post для add или edit form, валидация, uuid, данные update
    # ? исползуется в выводе связанных моделуй
    # ? dict['update'] - может ли данный модуль иметь возможность создерать несколько uuid. Например один телефон для многих заказов. Возвращате true false
    # ? how - sting -  add or edit parametr
    def checkRelatedFormDict(self, request_post, **kwargs):
        related = self.checkRelated()
        related_form_dict = {}
        if related:
            for x in related:
                _dict= dict()
                imp_related = importlib.import_module(x.module_name + '.related')
                getrelatedClass = getattr(imp_related, 'AppRelated')
                relatedClass = getrelatedClass()

                print('=================')
                if 'add' in kwargs['doing'] and relatedClass.passAddUpdate():
                    continue
                if 'edit' in kwargs['doing'] and relatedClass.passEditUpdate():
                    continue

                #_dict['module'] = x.module_name
                _dict['update'] = relatedClass.checkUpdate(request_post=request_post)


                if 'uuid' in kwargs:
                    _dict['convert'] = relatedClass.checkConvert(uuid=self.dictUuidToList(kwargs['uuid']),
                                                             request_post=request_post)
                    if 'edit' in kwargs['doing']:
                        _dict2 = relatedClass.checkRelatedEditForm(request_post=request_post, uuid=self.dictUuidToList(kwargs['uuid']))
                if 'add' in kwargs['doing']:
                    _dict2 = relatedClass.checkRelatedAddForm(request_post=request_post, request=kwargs['request'])
                    print('!self.request ', self.request)


                _dict['uuid'] = _dict2['uuid']
                _dict['pk'] = _dict2['pk']
                _dict['form'] = _dict2['form']
                _dict['class'] = relatedClass
                if _dict['form'].is_valid():
                    _dict['valid'] = True
                else:
                    _dict['valid'] = False
                related_form_dict[x.module_name] = _dict

        # помещаем в перменную есть ли общий валид или в какой-то из свазанных форм ест ошибка
        is_valid_dict = {}
        is_valid_dict['is_valid'] = True
        form_list = []
        for k, v in related_form_dict.items():
            if not v['valid']: is_valid_dict['is_valid'] = False
            form_list.append(v['form'])
        is_valid_dict['form'] = form_list
        return related_form_dict, is_valid_dict

    # [RU] получает dict из checkRelatedFormDict для сохранения формы в модель, после проверки валидности на этапе checkRelatedFormDict
    #
    #
    #
    def saveRelatedFormData(self, request, **kwargs):
        related_form_dict = kwargs['related_dict']
        related_uuid = kwargs['related_uuid']
        for k, v in related_form_dict.items():
            if related_form_dict[k]['update']:
                update_uuid_dict = related_form_dict[k]['uuid']
                update_uuid_dict.update(related_uuid)
                related_form_dict[k]['uuid'] = update_uuid_dict
            else:
                related_form_dict[k]['uuid'] = related_uuid
            relatedClass = related_form_dict[k]['class']
            relatedClass.saveForm(related_dict=related_form_dict[k])
        return


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
                    print('module' , _dict['module'])
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