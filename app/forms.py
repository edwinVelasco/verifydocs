from django import forms
from django.forms import ModelForm as BaseModelForm
from django.contrib.auth.models import User

from app.models import Dependence, UserMail, VerificationRequest

from app.models import DocumentType, Document, DocumentTypeUserMail


class VerifyDocsForm(forms.ModelForm):
    class Meta:
        model = VerificationRequest
        fields = ('verifier_name', 'verifier_email')
        error_messages = {
            'verifier_name': {
                'required': 'El nombre del verificador es necesario'
            },
            'verifier_email': {
                'required': 'El correo electrónico del verificador es necesario'
            }
        }

        widgets = {
            'verifier_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de empresa/persona solicitante',
                    'style': 'border-top-left-radius: 4px;border-bottom-left-radius: 4px; width: 100%;'
                }
            ),
            'verifier_email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                    'style': 'border-top-left-radius: 4px;border-bottom-left-'
                             'radius: 4px; width: 100%;',
                    'oninput': "compare_email()"
                }
            ),
        }
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Código seguro de verificación',
                'style': 'border-top-left-radius: 4px;border-bottom-left-radius: 4px;'
            }
        ), required=False
    )

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'hidden': True,
                'accept': '.pdf,.PDF'
            }
        ), required=False
    )

    verifier_email_two = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme el correo electrónico',
                'style': 'border-top-left-radius: 4px;border-bottom-left-'
                         'radius: 4px; width: 100%;',
                'oninput': "compare_email()"
            }
        )
    )

    def clean(self):
        if self.cleaned_data.get('verifier_email') != self.cleaned_data.get(
                'verifier_email_two'):
            self.add_error('verifier_email_two', 'El email no coincide')




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

    file_u = forms.FileField(widget=forms.FileInput(
                attrs={'accept': '.pdf,.PDF'}), required=False)

    def __init__(self, *args, **kwargs):
        super(DocumentTypeQRForm, self).__init__(*args, **kwargs)



    class Meta:
        model = DocumentType
        fields = ('pos_x', 'pos_y', 'scale')

        error_messages = {
            'pos_x': {
                'required': "La posición X es requerida.",
                'blank': 'Este valor no puede ser vacio'
            },
            'pos_y': {
                'required': "La posición Y es requerida.",
                'blank': 'Este valor no puede ser vacio'
            },
            'scale': {
                'required': 'Debe seleccionar una escala',
                'blank': 'Debe seleccionar una escala',
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
            'scale': forms.Select(
                attrs={'class': 'form-control'}
            )
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
        self.fields['password'].required = False

    class Meta:
        model = UserMail
        fields = ('email', 'role', 'active', 'password')

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
            'password': forms.PasswordInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Contraseña, Solo para aplicaciones'}
            )
        }

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()

    def clean(self):
        cleaned_data = super(UserMailForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")

        role = cleaned_data.get("role")

        if int(role) == 3:
            try:
                user = User.objects.get(username=self.instance.email)
            except User.DoesNotExist:
                if not password:
                    self.add_error('password',
                                   'El usuario de aplicación debe tener '
                                   'una contraseña')
        else:
            try:
                user = User.objects.get(username=email)
                user.delete()
            except User.DoesNotExist:
                pass
            finally:
                if password:
                    self.add_error('password',
                                   'El usuario no requiere contraseña')
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


class DocumentTypeUserMailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentTypeUserMailForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].required = True
        self.fields['usermail'].required = True
        self.fields['active'].required = True
        self.fields['document_type'].queryset = DocumentType.objects.filter(
            active=True)

    class Meta:
        model = DocumentTypeUserMail
        fields = ('usermail', 'active', 'document_type')

        error_messages = {
            '__all__': {
                'unique_together': 'El tipo de documento ya se encuentra '
                                   'registrado al usuario'
            },
            'usermail': {
                'required': "El correo es requerido."
            },
            'document_type': {
                'required': "El tipo de documento es requerido",
            },
        }

        widgets = {
            'usermail': forms.HiddenInput(),
            'active': forms.HiddenInput(),
            'document_type': forms.Select(
                attrs={'class': 'form-control',
                       'data-placeholder': 'Seleccionar Tipo de documento'},

            )
        }


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['identification_applicant'].required = True
        self.fields['name_applicant'].required = True
        self.fields['email_applicant'].required = True
        self.fields['expedition'].required = True
        self.fields['file_original'].required = True

        self.fields['expiration'].required = False
        self.fields['token'].required = False
        self.fields['hash'].required = False
        self.fields['hash_qr'].required = False
        self.fields['file_qr'].required = False

        self.fields['doc_type_user'].required = True
        self.fields['doc_type_user'].empty_label = 'Seleccione tipo de documento'

    class Meta:
        model = Document
        fields = ('identification_applicant', 'name_applicant',
                  'email_applicant', 'expedition', 'file_original',
                  'doc_type_user', 'token', 'hash', 'file_qr', 'hash_qr',
                  'expiration')

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
            'doc_type_user': {
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
            'doc_type_user': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'enable': forms.HiddenInput(),
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
    doc_type_user = forms.ModelChoiceField(
        queryset=DocumentTypeUserMail.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        empty_label='Tipos de documento',
    )
    is_enable = forms.BooleanField(
        widget=forms.CheckboxInput()
    )


class DocumentSearchAdminForm(forms.Form):
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


