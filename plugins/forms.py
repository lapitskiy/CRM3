from django import forms
from .models import Plugins
from django.utils.safestring import mark_safe
import re
from django.core.exceptions import ValidationError


#class CustomModelChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, obj):
#        return mark_safe("My Object custom label <strong>%i</strong>" % obj.id)


class RelatedPluginForm(forms.ModelForm):
    #query = Plugins.objects.values_list('module_name')
    #module_name = forms.ChoiceField(choices=(*query,))

    class Meta:
        model = Plugins
        fields = ['related',]
        #query = Plugins.objects.values_list('module_name')
        #widgets = {
          #  'module_name': forms.Select(choices=(*query,), attrs={'class': 'form-control'}),
         #   'module_name': forms.ChoiceField(choices=module_name),
         #   'module_name': forms.ModelChoiceField(queryset=Plugins.objects.all(), attrs={'class': 'form-control'}),
        #}

    def __init__(self, *args, **kwargs):
        super(RelatedPluginForm, self).__init__(*args, **kwargs)
        self.fields['related'] = forms.ModelChoiceField(label='', queryset=Plugins.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


   #relatedName = forms.ModelChoiceField(queryset=Plugins.objects.values_list('module_name'), required=False)
    #related = forms.ModelChoiceField(queryset=Plugins.objects.all(), label='Плагин', empty_label='Выбрать',
     #                                 widget=forms.Select(attrs={'class': 'form-control'}))

