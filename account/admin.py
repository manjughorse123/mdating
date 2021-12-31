from django.contrib import admin
from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email','mobile', 'name','otp', 'create_at')
    list_filter = ('email','mobile', 'name','create_at')
    readonly_fields = ('email', 'name','mobile', 'country_code','otp', 'birth_date', 'create_at')


admin.site.register(User, UserAdmin)
