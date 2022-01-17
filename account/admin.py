from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile', 'name', 'otp', 'is_phone_verified', 'id')
    list_filter = ('email', 'mobile', 'name')

# class UserInterestAdmin(admin.ModelAdmin):

#     list_display = ('interest','user')
    # list_filter = ('email', 'mobile', 'name')

# User = get_user_model()
admin.site.register(User, UserAdmin)
admin.site.register(Gender)
admin.site.register(Interest)
admin.site.register(MaritalStatus)
admin.site.register(UserIdealMatch)
admin.site.register(UserInterest)
admin.site.register(IdealMatch)


