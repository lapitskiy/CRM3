from django import forms
from .models import Prints

#forms
class SimplePrintAddForm(forms.ModelForm):

    class Meta:
        model = Prints
        fields = ['name', 'contentform']
