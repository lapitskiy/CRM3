from django import forms
from .models import Orders
import re
from django.core.exceptions import ValidationError


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        #fields = '__all__'
        fields = ['gadget', 'serial', 'status']
        widgets = {
            'gadget': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title