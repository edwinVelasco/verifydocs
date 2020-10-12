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


class UserMail(models.Model):
    email = models.EmailField(
        validators=[validate_domainonly_email, ],
        unique=True, )

    class Meta:
        verbose_name = 'Correo permitido'
        verbose_name_plural = 'Correos permitidos'
        ordering = ('email',)
        db_table = 'verifydocs_user_email'

    def __str__(self):
        return self.email


class ModelTracing(models.Model):
    updated = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Modificado')
    created = models.DateTimeField(auto_created=True, verbose_name='Creado')

class Dependence(ModelTracing):
    initials = models.CharField(max_length=3, verbose_name='siglas',
                                unique=True)
    name = models.CharField(max_length=255, verbose_name='Nombre', unique=True)

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'

