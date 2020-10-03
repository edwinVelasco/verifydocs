from django import forms
from django.forms import ModelForm as BaseModelForm


class VerifyDocsForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Código de verificación',
            }
        )
    )