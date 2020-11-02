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
        self.fields['days_validity'].required = False
        self.fields['active'].required = False
        self.fields['dependence'].required = True
        self.fields['dependence'].queryset = Dependence.objects.filter(
            active=True)
        self.fields['dependence'].empty_label = '--Seleccione dependencia--'

    class Meta:
        model = DocumentType
        fields = ('name', 'days_validity', 'active', 'dependence')

        error_messages = {
            'name': {
                'required': "El nombre es requerido.",
                'unique': 'El nombre ya se encuentra registrado'
            },
            'dependence': {
                'required': "La dependencia es requerida.",
            }
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre'}
            ),
            'dependence': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'days_validity': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Días de validez'}
            ),
            'active': forms.HiddenInput()
        }

    def clean_name(self):
        return self.cleaned_data.get('name', '').capitalize()


class DocumentTypeQRForm(forms.ModelForm):

    file = forms.FileField(widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(DocumentTypeQRForm, self).__init__(*args, **kwargs)



    class Meta:
        model = DocumentType
        fields = ('pos_x', 'pos_y')

        error_messages = {
            'pos_x': {
                'required': "La posición X es requerida.",
                'blank': 'Este valor no puede ser vacio'
            },
            'pos_y': {
                'required': "La posición Y es requerida.",
                'blank': 'Este valor no puede ser vacio'
            }
        }

        widgets = {
            'pos_x': forms.NumberInput(
                attrs={'class': 'form-control',
                       'value': '0', 'min': 0, 'step': 1}
            ),
            'pos_y': forms.NumberInput(
                attrs={'class': 'form-control',
                       'value': '0', 'min': 0, 'step': 1}
            ),
        }

    def clean(self):
        pos_y = self.cleaned_data['pos_y']
        if pos_y < 0:
            self.add_error('pos_y', 'El valor no puede ser inferior a 0')
        pos_x = self.cleaned_data['pos_x']
        if pos_x < 0:
            self.add_error('pos_x', 'El valor no puede ser inferior a 0')


class DocumentTypeSearchForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Nombre',
            'autocomplete': 'off'
        })
    )
    dependence = forms.ModelChoiceField(
        queryset=Dependence.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        empty_label='Dependencias',
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
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput()
    )


class DependenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DependenceForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['active'].required = False

    class Meta:
        model = Dependence
        fields = ('name', 'active')

        error_messages = {
            'name': {
                'required': "El nombre es requerido.",
                'unique': "Ya existe una dependencia con el mismo nombre.",
            },
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre',
                       'autofocus': True}
            ),
            'active': forms.HiddenInput()
        }

    def clean_name(self):
        return self.cleaned_data.get('name', '').capitalize()

    def clean(self):
        cleaned_data = super(DependenceForm, self).clean()
        return cleaned_data


class UserMailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserMailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = UserMail
        fields = ('email', 'role', 'active')

        error_messages = {
            'email': {
                'required': "El correo es requerido.",
                'unique': 'El correo ya se encuentra registrado'
            },
            'role': {
                'required': "Debe seleccionar un requerido.",
            },
        }

        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Correo electrónico',
                       'value': '@ufps.edu.co',
                       'autofocus': True}
            ),
            'role': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'active': forms.HiddenInput()
        }

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()


class UserMailSearchForm(forms.Form):
    ROLES_CHOICE = (
        ('', 'Seleccione el rol'),
        (1, 'Administrador'),
        (2, 'Administrativo'),
        (3, 'Aplicación'),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Correo',
            'autocomplete': 'off'
        })
    )
    role = forms.ChoiceField(
        choices=ROLES_CHOICE,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput()
    )
