from django import forms
from .models import Clients
import re
from django.core.exceptions import ValidationError

#fields
class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class RelatedAddForm(forms.ModelForm):
    #char_field_with_list = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        #_phone_list = kwargs.pop('data_list', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        listt = Clients.objects.all().order_by('-id').values_list('phone')
        self.fields['phone'].widget = ListTextWidget(data_list=listt, name='list_phone')

    class Meta:
        model = Clients
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            #'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }