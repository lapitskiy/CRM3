from django import forms
from .models import Storehouses, StoreRelated, Category
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .utils import getStoresListByUser

#forms
class StorehouseAddForm(forms.ModelForm):
    class Meta:
        model = Storehouses
        fields = ['name','address','phone','category',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'category': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        return name

class StorehouseAddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        return name

#forms
class StorehouseUserEditForm(forms.ModelForm):
    class Meta:
        model = Storehouses
        fields = ['user_permission',]

# если формы нет, как например в модуле prints, ставиться pass
class RelatedAddForm(forms.Form):
    name = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}), queryset=None)
    #related_uuid = forms.CharField(widget=forms.HiddenInput(), initial='value', required=False)
    #name = forms.ModelChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = getStoresListByUser(user=self.request.user)
        self.fields['name'].label = 'Склад'


    def save(self, **kwargs):
        #print('self name', self.name)
        #print('name', name)
        if 'commit' not in kwargs:
            data = self.cleaned_data
            #rec = StoreRelated(store=self.name, related_uuid=related_uuid)
            #rec.save()
            StoreRelated.objects.update_or_create(store=name, related_uuid=related_uuid)
            return data







