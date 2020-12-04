from django.contrib import admin
from app.models import UserMail


# Register your models here.


class UserMailAdmin(admin.ModelAdmin):
    fields = ('email', 'role', 'active', 'updated', 'created', 'password')
    readonly_fields = ('updated', 'created')
    list_display = ['email', 'role', 'active']


admin.site.register(UserMail, UserMailAdmin)


