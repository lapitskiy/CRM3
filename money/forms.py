from django import forms
from .models import Money, Prepayment

class RelatedAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Money
        fields = ['money',]
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }

class MoneyEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MoneyEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Money
        fields = ['money',]
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
        labels = {
        }

class PrepayEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PrepayEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Prepayment
        fields = ['prepayment','comment']
        widgets = {
            'prepayment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
        }

