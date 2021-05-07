from django import forms
from .models import Orders, Service, Device
import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist

#fields
class ListTextWidget(forms.Select):
    template_name = 'include/_forms_orders_datalist.html'

    def format_value(self, value):
        # Copied from forms.Input - makes sure value is rendered properly
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
    service = ChoiceTxtField(queryset=Service.objects.all().order_by('-id'))
    device = ChoiceTxtField(queryset=Device.objects.all().order_by('-id'))

    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'status','comment']
        widgets = {
            #'category': forms.Select(attrs={'class': 'form-control'}),
                #forms.HiddenInput(),
            #'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            #'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'status': forms.Select(attrs={'class': 'form-control', 'autocomplete':'on'}),
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
    class Meta:
        model = Orders
        fields = ['device', 'serial', 'service', 'comment']
        widgets = {
            'device': forms.TextInput(attrs={'id':'ajax-device', 'class': 'form-control', 'autocomplete':'off'}),
            'service': forms.TextInput(attrs={'id':'ajax-service', 'class': 'form-control', 'autocomplete':'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
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