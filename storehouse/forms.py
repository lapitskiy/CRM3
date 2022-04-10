from django import forms
from .models import Storehouses, StoreRelated, Category
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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

# если формы нет, как например в модуле prints, ставиться pass
class RelatedAddForm(forms.ModelForm):

    class Meta:
        model = StoreRelated
        fields = ['store']
        widgets = {
            'store': forms.HiddenInput(),
            'name': forms.Select(attrs={'class': 'form-control', 'autocomplete':'on'}),
        }
        labels = {
        }