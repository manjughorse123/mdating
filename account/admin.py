from django.contrib import admin
from .models import *
# from django.contrib.auth import get_user_model


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile', 'name', 'otp', 'is_phone_verified')
    list_filter = ('email', 'mobile', 'name')


# User = get_user_model()
admin.site.register(User, UserAdmin)
