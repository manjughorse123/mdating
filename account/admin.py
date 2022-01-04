from django.contrib import admin
from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile', 'name', 'otp', 'userid', 'create_at', 'is_phone_verified')
    list_filter = ('email', 'mobile', 'name', 'create_at')
    readonly_fields = ('email', 'name', 'mobile', 'country_code', 'otp', 'birth_date', 'create_at', 'is_phone_verified')


admin.site.register(User, UserAdmin)
