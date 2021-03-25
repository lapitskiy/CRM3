from django import forms
from .models import Money

class RelatedAddForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['money', 'prepayment']
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'prepayment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }