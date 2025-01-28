from django import forms
from .models import Prints
from django_ckeditor_5.widgets import CKEditor5Widget

#forms
class SimplePrintAddForm(forms.ModelForm):
    contentform = forms.CharField(
        widget=CKEditor5Widget(  # <- Исправлено
            config_name='default',
            attrs={"class": "django_ckeditor_5"},
        ),
        label="Контент",
    )

    class Meta:
        model = Prints
        fields = ['name', 'contentform']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }

class RelatedAddForm:
    pass