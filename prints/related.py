#from .forms import RelatedAddForm
from .models import Prints
from django.db.models import Q

class AppRelated(object):
    prefix = 'prints'
    related_module_name = 'prints'
    related_format = 'link' # показывает это или форма будет или просто связанные данные в виде текста или ссылки
    related_data_format = 'link'

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passAddUpdate(self, **kwargs):
        return True

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passEditUpdate(self, **kwargs):
        return True

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обрабтока такой возможности
    def checkUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # return False or dict uudi convert
    def checkConvert(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        pass

    def checkRelatedEditForm(self, **kwargs):
        pass

    def deleteRelatedMultipleUuid(self, **kwargs):
        pass

    def submenuImportRelated(self, **kwargs):
        pass

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True

    def saveForm(self, **kwargs):
        pass

    def linkGetReleatedData(self, **kwargs):
        pass
