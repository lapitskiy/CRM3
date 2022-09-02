from django import forms
from .models import Orders, Service, Device, Category_service, Status
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .utils import getActiveStatus, getCategoryServicePermission

#fields
class ListTextWidget(forms.Select):
    template_name = 'include/_forms_orders_datalist.html'

    def format_value(self, value):
        if value == '' or value is None:
            return ''
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)

class ChoiceTxtField(forms.ModelChoiceField):
    widget=ListTextWidget()

#forms
class SimpleOrderAddForm(forms.ModelForm):
    #service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=ListTextWidget())
    service = ChoiceTxtField(queryset=Service.objects.order_by('-used'))
    device = ChoiceTxtField(queryset=Device.objects.order_by('-used'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SimpleOrderAddForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = getActiveStatus()
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['',]
        self.fields['status'].choices = [(k, v) for k, v in self.fields['status'].choices if k not in status_excluded]
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]
        self.fields['service'].choices = [(k, v) for k, v in self.fields['service'].choices if k not in status_excluded]
        self.fields['device'].choices = [(k, v) for k, v in self.fields['device'].choices if k not in status_excluded]
        self.fields['service'].label = 'Услуга'
        self.fields['device'].label = 'Устройство'

    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'status', 'comment', 'category_service']
        widgets = {
            #'category': forms.Select(attrs={'class': 'form-control'}),
                #forms.HiddenInput(),
            #'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            #'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'status': forms.Select(attrs={'class': 'form-control', 'autocomplete':'on'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean(self):
        cleaned_data = super(SimpleOrderAddForm, self).clean()
        service = cleaned_data.get("service")
        if service:
            print('service ', service)

    def clean_service(self):
        name = self.cleaned_data['service']
        print('name ', str(self.cleaned_data['service'].pk))
        return name



class FastOrderAddForm(forms.ModelForm):
    service = ChoiceTxtField(queryset=Service.objects.all().order_by('-id'))
    device = ChoiceTxtField(queryset=Device.objects.all().order_by('-id'))


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FastOrderAddForm, self).__init__(*args, **kwargs)
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['',]
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]
        self.fields['service'].label = 'Услуга'
        self.fields['device'].label = 'Устройство'



    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'category_service']
        widgets = {
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
        }



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

class SettingCategoryServiceAddForm(forms.ModelForm):
    class Meta:
        model = Category_service
        fields = ['name','category','user_permission']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        if not name[0].isupper():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name

class SettingStatusAddForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['title', 'active_creation']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'active_creation': forms.CheckboxInput(),
        }
        labels = {
            'active_creation': 'Активно при создании заказа',
        }

    def clean_name(self):
        name = self.cleaned_data['title']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        if not name[0].isupper():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name