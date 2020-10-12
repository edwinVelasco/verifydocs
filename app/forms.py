from django import forms
from django.forms import ModelForm as BaseModelForm

from app.models import Dependence


class VerifyDocsForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Código de verificación',
                'style': 'border-top-left-radius: 4px;border-bottom-left-radius: 4px;'
            }
        )
    )


class DependenceForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
            }
        )
    )

    class Meta:
        model = Dependence
        fields = ['name']