from django import forms
from .models import Clients
import re
from django.core.exceptions import ValidationError

class RelatedAddForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }