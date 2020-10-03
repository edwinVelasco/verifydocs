from django.db import models
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
# Create your models here.
class Doc(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='docs', storage=gd_storage)
