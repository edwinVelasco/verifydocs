from django.contrib import admin
from app.models import UserMail, Dependence, Document


# Register your models here.


class DocumentAdmin(admin.ModelAdmin):
    fields = ('identification_applicant', 'name_applicant', 'email_applicant',
              'expedition', 'file_original', 'document_type', 'enable')


class UserMailAdmin(admin.ModelAdmin):
    fields = ('email', 'role', 'active', 'updated', 'created','password')
    readonly_fields = ('updated', 'created')
    list_display = ['email', 'role', 'active']


class DependenceAdmin(admin.ModelAdmin):
    fields = ('name',)


admin.site.register(Document, DocumentAdmin)
admin.site.register(UserMail, UserMailAdmin)
admin.site.register(Dependence, DependenceAdmin)


