from django.contrib import admin
from app.models import Doc
# Register your models here.

class DocAdmin(admin.ModelAdmin):
    fields = ('name', 'file')

admin.site.register(Doc, DocAdmin)