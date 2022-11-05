from django import forms
from .models import Money

class RelatedAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Money
        fields = ['money', 'prepayment']
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'prepayment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }

