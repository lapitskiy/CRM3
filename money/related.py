from .forms import RelatedAddForm
from .models import Money

class checkRelated(object):
    prefix = 'money'

    def checkUpdate(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        context = {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            pass
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            context['uuid'] = ''
        print('request_post ', request_post)
        print('related_form ', related_form)
        context['form'] = related_form
        return context
