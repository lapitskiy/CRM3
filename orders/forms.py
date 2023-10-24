from django import forms
from .models import Orders, Service, Device, Category_service, Status
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .utils import getActiveStatus, getCategoryServicePermission
from django_select2 import forms as s2forms

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
    widget = ListTextWidget()

#forms

class DeviceSelect2Widget(s2forms.ModelSelect2Widget):
    queryset = Device.objects.all()
    #print('tyt', queryset)
    search_fields = [
        'name__icontains',
    ]

'''
# TRY REDIS SELECT2
class SimpleOrderAddForm(forms.ModelForm):
    device = forms.ModelChoiceField(widget=DeviceSelect2Widget(attrs={'class': 'select2'}), queryset=Device.objects.all().order_by('used'))
    #device = forms.ModelChoiceField(widget=DeviceSelect2Widget(attrs={'class': 'select2'}))
    #device = forms.ModelChoiceField(widget=DeviceSelect2Widget, queryset=Device.objects.all().order_by('used'))
    #device = DeviceSelect2Widget(attrs={'class': 'select2'})
    #print('tyt2', device)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SimpleOrderAddForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = getActiveStatus()
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['','-']
        self.fields['status'].choices = [(k, v) for k, v in self.fields['status'].choices if k not in status_excluded]
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]

        #self.fields['device'] = ChoiceTxtField(queryset=Device.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'] = ChoiceTxtField(queryset=Service.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'].choices = [(k, v) for k, v in self.fields['service'].choices if k not in status_excluded]
        #self.fields['device'].choices = [(k, v) for k, v in self.fields['device'].choices if k not in status_excluded]
        #self.fields['device'] = ChoiceSelect2Field(queryset=Device.objects.all().order_by('used'))
        #print(self.fields['device'])
        self.fields['service'].label = 'Услуга'
        self.fields['device'].label = 'Устройство'

    class Meta:
        model = Orders
        fields = ['category_service', 'device', 'serial', 'service', 'status', 'comment']
        widgets = {
            #'category': forms.Select(attrs={'class': 'form-control'}),
                #forms.HiddenInput(),
            #'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            #'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            #'device': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
            #'device': DeviceSelect2Widget(queryset=Device.objects.all()),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'status': forms.Select(attrs={'class': 'form-control', 'autocomplete':'on'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

'''

class SimpleOrderAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SimpleOrderAddForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = getActiveStatus()
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['','-']
        self.fields['status'].choices = [(k, v) for k, v in self.fields['status'].choices if k not in status_excluded]
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]

        self.fields['device'] = ChoiceTxtField(queryset=Device.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'] = ChoiceTxtField(queryset=Service.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'].choices = [(k, v) for k, v in self.fields['service'].choices if k not in status_excluded]
        self.fields['device'].choices = [(k, v) for k, v in self.fields['device'].choices if k not in status_excluded]
        self.fields['service'].label = 'Услуга'
        self.fields['device'].label = 'Устройство'

    class Meta:
        model = Orders
        fields = ['category_service', 'device', 'serial', 'service', 'status', 'comment']
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



#forms
class SimpleOrderEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SimpleOrderEditForm, self).__init__(*args, **kwargs)
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['','-']
        self.fields['status'].choices = [(k, v) for k, v in self.fields['status'].choices if k not in status_excluded]
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]
        self.fields['device'] = ChoiceTxtField(queryset=Device.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'] = ChoiceTxtField(queryset=Service.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'].choices = [(v, k) for k, v in self.fields['service'].choices if k not in status_excluded]
        #self.fields['service'].choices = [(k.id, str(k)) for k in self.fields['service'].choices if k not in status_excluded]
        self.fields['device'].choices = [(k, v) for k, v in self.fields['device'].choices if k not in status_excluded]
        self.fields['service'].label = 'Услуга'
        self.fields['device'].label = 'Устройство'

    class Meta:
        model = Orders
        fields = ['category_service', 'device', 'serial', 'service', 'status', 'comment']

        widgets = {
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'status': forms.Select(attrs={'class': 'form-control', 'autocomplete':'on'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean(self):
        return super(SimpleOrderEditForm, self).clean()

class FastOrderAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #print('tyt2 ')
        self.request = kwargs.pop('request', None)
        super(FastOrderAddForm, self).__init__(*args, **kwargs)
        self.fields['category_service'].queryset = getCategoryServicePermission(user=self.request.user)
        status_excluded = ['','-']
        self.fields['category_service'].choices = [(k, v) for k, v in self.fields['category_service'].choices if k not in status_excluded]
        self.fields['device'] = ChoiceTxtField(queryset=Device.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'] = ChoiceTxtField(queryset=Service.objects.filter(category_service__in=self.fields['category_service'].queryset).order_by('-used'))
        self.fields['service'].choices = [(k, v) for k, v in self.fields['service'].choices if k not in status_excluded]
        self.fields['device'].choices = [(k, v) for k, v in self.fields['device'].choices if k not in status_excluded]
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
        fields = ['name','category_service']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
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
        fields = ['name','category_service']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'category_service': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'on'}),
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
        fields = ['name','user_permission']
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

class SettingStatusAddForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['title', 'active_creation', 'closed_status', 'fast_closed', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'active_creation': forms.CheckboxInput(),
            'closed_status': forms.CheckboxInput(),
            'fast_closed': forms.CheckboxInput(),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'closed_status': 'Статус закрывает заказ',
            'active_creation': 'Активно при создании заказа',
            'fast_closed': 'Быстрое закрытие заказов',
        }

    def clean_name(self):
        name = self.cleaned_data['title']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        if not name[0].isupper():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name