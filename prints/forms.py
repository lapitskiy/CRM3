from django import forms
from .models import Prints
from ckeditor.widgets import CKEditorWidget

#forms
class SimplePrintAddForm(forms.ModelForm):
    contentform = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Prints
        fields = ['name', 'contentform']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
        }
