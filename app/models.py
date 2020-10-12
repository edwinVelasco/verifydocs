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



