from django import forms
from .models import Orders
import re
from django.core.exceptions import ValidationError

class OrderAddForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['device', 'serial', 'comment', 'status']
        widgets = {
            'device': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_device(self):
        device = self.cleaned_data['device']
        if re.match(r'\d', device):
            raise ValidationError('Название не должно начинаться с цифры')
        return device