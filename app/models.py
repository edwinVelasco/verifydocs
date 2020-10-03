from django.db import models
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import EmailValidator

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
# Create your models here.


class Doc(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='docs', storage=gd_storage)


class UserMail(models.Model):
    email = models.EmailField(
        validators=[EmailValidator(message='El correo no pertenece a la UFPS',
                                   whitelist=['@ufps.edu.co']), ],
        unique=True, )

    class Meta:
        verbose_name = 'Correo permitido'
        verbose_name_plural = 'Correos permitidos'
        ordering = ('email',)
        db_table = 'verifydocs_user_email'

    def __str__(self):
        return self.email
