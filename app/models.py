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
    acronym = models.CharField(max_length=4, verbose_name='Acrónimo',
                               unique=True)
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
        return f'{self.name} - {self.acronym}'


class UserMail(models.Model):
    email = models.EmailField(
        validators=[validate_domainonly_email, ],
        unique=True, verbose_name='Correo')
    dependence = models.ForeignKey(Dependence, on_delete=models.PROTECT,
                                   verbose_name='Dependencia', null=True,
                                   blank=True,
                                   related_name='users_mail')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Es administrador')
    active = models.BooleanField(default=False,
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
        return f'{self.email} - {self.dependence or "Sin dependencia"}'

    def update_active(self):
        self.active = not self.active
        self.save()


class DocumentType(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=4, unique=True)
    days_validity = models.IntegerField(default=None, null=True, blank=True)
    active = models.BooleanField(default=True)

    def update_active(self):
        self.active = not self.active
        self.save()

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'
        ordering = ('name',)
        db_table = 'verifydocs_document_type'

    def __str__(self):
        return f'"{self.name} - {self.acronym}"'
