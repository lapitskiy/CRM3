from .forms import RelatedAddForm
from .models import Money

class checkRelated(object):
    prefix = 'money'

    def checkUpdate(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        if self.checkUpdate(request_post=kwargs['request_post']):
            pass
        else:
            related_form = RelatedAddForm(kwargs['request_post'], prefix=self.prefix)
            related_form.prefix = self.prefix
        print('request_post ', kwargs['request_post'])
        print('related_form ', related_form)
        return related_form
