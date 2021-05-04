from django import forms
from .models import Orders, Service, Device
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class SimpleOrderAddForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'status','comment']
        widgets = {
            #'category': forms.Select(attrs={'class': 'form-control'}),
                #forms.HiddenInput(),
            'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_service(self):
        name = self.cleaned_data['service']
        print('clean ')
        print('name ', name)
        try:
            get_service = Service.objects.get(name=name)
            print('get_service ', get_service)
            return get_service.pk
        except get_service.DoesNotExist:
            return name
        return name


class FastOrderAddForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'comment']
        widgets = {
            'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_service(self):
        name = self.cleaned_data['service']
        print('name ', name)
        try:
            get_service = Service.objects.get(name=name)
            print('get_service ', get_service)
            return get_service.pk
        except get_service.DoesNotExist:
            return name


class SettingServiceAddForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        if not name[0].isupper():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name

class SettingDeviceAddForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        if not name[0].isupper():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name