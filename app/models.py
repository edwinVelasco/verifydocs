from django.db import models
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import EmailValidator
from app.validators import validate_domainonly_email

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
# Create your models here.


class Dependence(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    active = models.BooleanField(default=True, verbose_name='Activo')

    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Última modificación')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'
        ordering = ('name',)
        db_table = 'verifydocs_dependence'

    def update_active(self):
        self.active = not self.active
        self.save()

    def __str__(self):
        return self.name.capitalize()


class DocumentType(models.Model):
    CHOICES_SCALE = (
        (42, '1x'),
        (63, '1.5x'),
        (84, '2x'),
    )
    name = models.CharField(max_length=45, unique=True)
    days_validity = models.IntegerField(default=None, null=True, blank=True)
    active = models.BooleanField(default=True)
    dependence = models.ForeignKey(Dependence, on_delete=models.PROTECT,
                                   verbose_name='Dependencia', null=True,
                                   blank=True,
                                   related_name='dependence_docs_type')
    pos_x = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    pos_y = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    scale = models.IntegerField(null=True,
                                choices=CHOICES_SCALE)
    updated = models.DateTimeField(auto_now=True,
                                   null=False,
                                   verbose_name='Última modificación')
    created = models.DateTimeField(auto_now_add=True,
                                   null=False,
                                   verbose_name='Creado')

    def update_active(self):
        self.active = not self.active
        self.save()

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'
        ordering = ('name',)
        db_table = 'verifydocs_document_type'

    def __str__(self):
        return f'{self.name.capitalize()}'


class UserMail(models.Model):
    ROLES_CHOICE = (
        (1, 'Administrador'),
        (2, 'Administrativo'),
        (3, 'Aplicación'),
    )
    email = models.EmailField(
        validators=[validate_domainonly_email, ],
        unique=True, verbose_name='Correo')
    role = models.IntegerField(choices=ROLES_CHOICE, null=True,
                               verbose_name='Rol')
    active = models.BooleanField(default=True,
                                 verbose_name='Activo')

    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Última modificación')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    document_types = models.ManyToManyField(
        DocumentType, related_name="verifydocs_user_doc_type")

    class Meta:
        verbose_name = 'Correo permitido'
        verbose_name_plural = 'Correos permitidos'
        ordering = ('-updated',)
        db_table = 'verifydocs_user_email'

    def __str__(self):
        return self.email

    def update_active(self):
        self.active = not self.active
        self.save()


class Document(models.Model):
    identification_applicant = models.CharField(max_length=10, null=False,
                                                blank=False)
    name_applicant = models.CharField(max_length=45, null=False, blank=False)
    email_applicant = models.EmailField(max_length=45, null=False, blank=False)
    expedition = models.DateField(null=False, blank=False)
    file_original = models.FileField(upload_to='docs_original',
                                     storage=gd_storage)

    token = models.CharField(max_length=32, null=False, blank=False,
                             unique=True)
    hash = models.CharField(max_length=64, null=False, blank=False,
                            unique=True)
    hash_qr = models.CharField(max_length=64, null=False, blank=False,
                               unique=True)
    expiration = models.DateField(null=True, blank=True, default=None)
    file_qr = models.FileField(upload_to='docs_qr', storage=gd_storage)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT,
                                      verbose_name='Tipo de documento',
                                      related_name='dependence_docs_type')
    user_mail = models.EmailField(max_length=45, default='')
    enable = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ('-id',)
        db_table = 'verifydocs_document'

    def update_active(self):
        self.enable = not self.enable
        self.save()

