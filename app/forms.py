from django import forms
from django.forms import ModelForm as BaseModelForm

from app.models import Dependence, UserMail

from app.models import DocumentType, Document


class VerifyDocsForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Código seguro de verificación',
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
        self.fields['document_types'].required = False
        self.fields['document_types'].queryset = DocumentType.objects.filter(
            active=True)

    class Meta:
        model = UserMail
        fields = ('email', 'role', 'active', 'document_types')

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
            'active': forms.HiddenInput(),
            'document_types': forms.SelectMultiple(
                attrs={'class': 'chosen-select',
                       'multiple': 'multiple',
                       'data-placeholder': 'Seleccionar Tipos de documentos'},

            )
        }

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()

    def clean(self):
        cleaned_data = super(UserMailForm, self).clean()
        document_types = cleaned_data.get("document_types")
        role = cleaned_data.get("role")
        if int(role) == 1 and document_types:
            self.add_error('document_types',
                           'El usuario administrador no debe tener documentos')
        return cleaned_data


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


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['identification_applicant'].required = True
        self.fields['name_applicant'].required = True
        self.fields['email_applicant'].required = True
        self.fields['expedition'].required = True
        self.fields['file_original'].required = True

        self.fields['token'].required = False
        self.fields['hash'].required = False
        self.fields['hash_qr'].required = False
        self.fields['file_qr'].required = False

        self.fields['document_type'].required = True
        self.fields['document_type'].empty_label = 'Seleccione tipo de documento'

    class Meta:
        model = Document
        fields = ('identification_applicant', 'name_applicant',
                  'email_applicant', 'expedition', 'file_original',
                  'document_type', 'user_mail', 'token', 'hash', 'file_qr',
                  'hash_qr')

        error_messages = {
            'identification_applicant': {
                'required': "La identificación del solicitante es requerida."
            },
            'name_applicant': {
                'required': "El nombre del solicitante es requerido.",
            },
            'email_applicant': {
                'required': "El correo electrónico del solicitante "
                            "es requerido.",
            },
            'expedition': {
                'required': "La fecha de expedición es requerida.",
            },
            'file_original': {
                'required': "El documento en PDF es requerido.",
            },
            'document_type': {
                'required': "El tipo de documento es requerido.",
            },
            'hash_qr': {
                'unique': 'El documento ya se encuentra registrado'
            },
            'hash': {
                'unique': 'El documento ya se encuentra registrado'
            },
            'token': {
                'unique': 'El documento ya se encuentra registrado'
            }

        }

        widgets = {
            'identification_applicant': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Código estudiante / Identificación'}
            ),
            'name_applicant': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre'}
            ),
            'email_applicant': forms.EmailInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Correo electrónico'}
            ),
            'expedition': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Fecha',
                       'readonly': ''}
            ),
            'file_original': forms.FileInput(
                attrs={'accept': '.pdf,.PDF'}
            ),
            'document_type': forms.Select(
                attrs={'class': 'form-control chosen-select'}
            ),
            'enable': forms.HiddenInput(),
            'user_mail': forms.HiddenInput(),
            'token': forms.HiddenInput(),
            'hash': forms.HiddenInput(),
            'hash_qr': forms.HiddenInput(),
            'file_qr': forms.FileInput(
                attrs={'accept': '.pdf,.PDF'}
            ),
        }

    def clean_name(self):
        return self.cleaned_data.get('name', '').capitalize()

    def clean(self):
        cleaned_data = super(DocumentForm, self).clean()
        identification = cleaned_data.get("identification_applicant")
        try:
            identification = int(identification)
        except Exception as e:
            self.add_error('identification_applicant',
                           'La identificación del solicitante debe ser '
                           'numerica')
        return cleaned_data


class DocumentSearchForm(forms.Form):
    id = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control col-md-2', 'placeholder': 'ID',
                'autocomplete': 'off'
            }
        )
    )

    applicant = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Solicitante',
            'autocomplete': 'off'
        })
    )
    expedition = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control',
                                      'placeholder': 'Expedición',
                                      'readonly': ''}
                               )
    )
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        empty_label='Tipos de documento',
    )
    is_enable = forms.BooleanField(
        widget=forms.CheckboxInput()
    )


