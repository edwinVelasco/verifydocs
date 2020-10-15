from django import forms
from django.forms import ModelForm as BaseModelForm

from app.models import Dependence, UserMail

from app.models import DocumentType


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


class DocumentTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentTypeForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['acronym'].required = True
        self.fields['days_validity'].required = False
        self.fields['active'].required = False

    class Meta:
        model = DocumentType
        fields = ('__all__')

        error_messages = {
            'name': {
                'required': "El nombre es requerido.",
            },
            'acronym': {
                'required': "El acrónimo es requerido.",
                'unique': 'El acrónimo ya se encuentra registrado'
            }
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre'}
            ),
            'acronym': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Acrónimo'}
            ),
            'days_validity': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Días de validez'}
            ),
            'active': forms.HiddenInput()
        }

    def clean_acronym(self):
        return self.cleaned_data.get('acronym', '').upper()

    def clean_name(self):
        return self.cleaned_data.get('name', '').capitalize()

    def clean(self):
        cleaned_data = super(DocumentTypeForm, self).clean()
        acronym = cleaned_data.get('acronym', '')
        if len(acronym) < 4:
            self.add_error('acronym',
                           'El acrónimo debe tener cuatro caracteres')

        return cleaned_data


class DocumentTypeSearchForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Nombre',
            'autocomplete': 'off'
        })
    )
    acronym = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Acrónimo',
            'autocomplete': 'off'
        })
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput()
    )


class DependenceSearchForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Nombre',
            'autocomplete': 'off'
        })
    )
    acronym = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Acrónimo',
            'autocomplete': 'off'
        })
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput()
    )


class DependenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DependenceForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['acronym'].required = True
        self.fields['active'].required = False

    class Meta:
        model = Dependence
        fields = ('name', 'acronym', 'active')

        error_messages = {
            'name': {
                'required': "El nombre es requerido.",
            },
            'acronym': {
                'required': "El acrónimo es requerido.",
                'unique': 'El acrónimo ya se encuentra registrado'
            }
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre'}
            ),
            'acronym': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Acrónimo'}
            ),
            'active': forms.HiddenInput()
        }

    def clean_acronym(self):
        return self.cleaned_data.get('acronym', '').upper()

    def clean_name(self):
        return self.cleaned_data.get('name', '').capitalize()

    def clean(self):
        cleaned_data = super(DependenceForm, self).clean()
        acronym = cleaned_data.get('acronym', '')
        if len(acronym) < 4:
            self.add_error('acronym',
                           'El acrónimo debe tener cuatro caracteres')

        return cleaned_data


class UserMailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserMailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['dependence'].required = False
        self.fields['dependence'].queryset = Dependence.objects.filter(
            active=True)

    class Meta:
        model = UserMail
        fields = ('email', 'dependence', 'is_staff')

        error_messages = {
            'email': {
                'required': "El correo es requerido.",
                'unique': 'El correo ya se encuentra registrado'
            }
        }

        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Correo electrónico'}
            ),
            'dependence': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'is_staff': forms.CheckboxInput(attrs={})
        }

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()


class UserMailSearchForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Correo',
            'autocomplete': 'off'
        })
    )
    dependence = forms.ModelChoiceField(
        queryset=Dependence.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    is_staff = forms.BooleanField(
        widget=forms.CheckboxInput()
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput()
    )
