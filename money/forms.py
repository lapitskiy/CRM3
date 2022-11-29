from django import forms
from .models import Money, Prepayment

class InputTextWidget(forms.TextInput):
    template_name = 'include/_forms_textinput.html'

    def format_value(self, value):
        if value == '' or value is None:
            return ''
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)

class MyInputText(forms.TextInput):
    widget = InputTextWidget()

class RelatedAddForm(forms.ModelForm):
    #money = MyInputText()
    is_pay = forms.BooleanField(initial=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)
        self.fields['money'].initial = ''
        self.fields['is_pay'].label = 'Оплачено'

    class Meta:
        model = Money
        fields = ['money', 'is_pay']
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'Стоимость'}),
            'is_pay': forms.CheckboxInput()
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
        self.fields['prepayment'].initial = ''

    class Meta:
        model = Prepayment
        fields = ['prepayment','comment']
        widgets = {
            'prepayment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'Предоплата'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'prepayment': 'Принять предоплату',
        }

    #def clean_prepayment(self):
        #prepayment = self.cleaned_data['prepayment']
        #if prepayment == '' or prepayment <= 0:
        #    raise ValidationError('Поле не должно быть нулевым или пустым')

