from django.db import models
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import EmailValidator
from app.validators import validate_domainonly_email

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
# Create your models here.


class Doc(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='docs', storage=gd_storage)


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

    class Meta:
        verbose_name = 'Correo permitido'
        verbose_name_plural = 'Correos permitidos'
        ordering = ('-updated',)
        db_table = 'verifydocs_user_email'

    def __str__(self):
        return f'{self.email}'

    def update_active(self):
        self.active = not self.active
        self.save()


class DocumentType(models.Model):
    name = models.CharField(max_length=45, unique=True)
    days_validity = models.IntegerField(default=None, null=True, blank=True)
    active = models.BooleanField(default=True)
    dependence = models.ForeignKey(Dependence, on_delete=models.PROTECT,
                                   verbose_name='Dependencia', null=True,
                                   blank=True,
                                   related_name='dependence_docs_type')
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
        return self.name.capitalize()
