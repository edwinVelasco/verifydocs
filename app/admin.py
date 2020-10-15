from django.contrib import admin
from app.models import Doc, UserMail, Dependence


# Register your models here.


class DocAdmin(admin.ModelAdmin):
    fields = ('name', 'file')


class UserMailAdmin(admin.ModelAdmin):
    fields = ('email', 'dependence', 'is_staff', 'updated', 'created')
    readonly_fields = ('updated', 'created')
    list_display = ['email', 'dependence', 'is_staff']


class DependenceAdmin(admin.ModelAdmin):
    fields = ('name',)


admin.site.register(Doc, DocAdmin)
admin.site.register(UserMail, UserMailAdmin)
admin.site.register(Dependence, DependenceAdmin)


