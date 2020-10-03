from django.contrib import admin
from app.models import Doc, UserMail
# Register your models here.


class DocAdmin(admin.ModelAdmin):
    fields = ('name', 'file')


class UserMailAdmin(admin.ModelAdmin):
    fields = ('email', )


admin.site.register(Doc, DocAdmin)
admin.site.register(UserMail, UserMailAdmin)


