from django import forms
from .models import Clients
import copy
import re
from django.core.exceptions import ValidationError
from django.db.models import Q

#fields
class ListTextWidget(forms.Select):
    template_name = 'include/_forms_clients_datalist.html'

    def format_value(self, value):
        # Copied from forms.Input - makes sure value is rendered properly
        if value == '' or value is None:
            print('ListTextWidget None')
            return ''
        if self.is_localized:
            print('ListTextWidget local')
            return formats.localize_input(value)
        return str(value)

#class ChoiceTxtField(forms.ModelChoiceField):
#    widget=ListTextWidget()

class PhoneInputField(forms.CharField):
    widget=ListTextWidget()

class RelatedAddForm(forms.ModelForm):
    phone = PhoneInputField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].choices = Clients.objects.order_by('-phone').values_list('phone')

    #phone = ChoiceTxtField(queryset=Clients.objects.order_by('-phone'))

    class Meta:
        model = Clients
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            # 'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }

# ВТОРОЙ ВАРИАНТ
#fields2 второй вариант
#
#
class ListTextWidget2(forms.TextInput):
    def __init__(self, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        #self._list = data_list
        #self.attrs.update({'list':'list__%s' % self._name})
        self.attrs.update({'value': '+7', 'autocomplete': 'off'})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        #for item in self._list:
        #    data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class RelatedAddForm2(forms.ModelForm):
    #char_field_with_list = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        #_phone_list = kwargs.pop('data_list', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        #listt = Clients.objects.all().order_by('-id').values_list('phone')
        self.fields['phone'].widget = ListTextWidget(name='list_phone') #(data_list=listt, name='list_phone')

    class Meta:
        model = Clients
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            #'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }



