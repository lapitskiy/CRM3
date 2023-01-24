from django import forms
from .models import Money, Prepayment

class is_pay_SpecialCheckboxInput(forms.CheckboxInput):
    template_name = "include/_forms_textinput.html"

class card_pay_SpecialCheckboxInput(forms.CheckboxInput):
    template_name = "include/_forms_textinput_card.html"

class RelatedAddForm(forms.ModelForm):
    #money = MyInputText()
    is_pay = forms.BooleanField(label=False, initial=True, required=False, widget=is_pay_SpecialCheckboxInput(attrs={}))
    card_pay = forms.BooleanField(label=False, initial={'card_pay':True}, required=False, widget=card_pay_SpecialCheckboxInput(attrs={}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RelatedAddForm, self).__init__(*args, **kwargs)
        self.fields['money'].initial = ''

    class Meta:
        model = Money
        fields = ['money', 'card_pay', 'is_pay']
        widgets = {
            'money': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'Стоимость'}),
            #'is_pay': forms.CheckboxInput(attrs={'class': 'text-danger', 'required': 'False'})
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
            'prepayment': 'Принять оплату',
        }

    #def clean_prepayment(self):
        #prepayment = self.cleaned_data['prepayment']
        #if prepayment == '' or prepayment <= 0:
        #    raise ValidationError('Поле не должно быть нулевым или пустым')

