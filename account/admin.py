from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile', 'name', 'otp', 'is_phone_verified', 'location', 'id', 'create_at', 'update_at')
    list_filter = ('email', 'mobile', 'name', 'create_at')
    # readonly_fields =  ('email', 'mobile', 'name', 'otp', 'is_phone_verified', 'location','id', 'create_at', 'update_at')


admin.site.register(User, UserAdmin)


class GenderAdmin(admin.ModelAdmin):
    list_display = ('gender', 'id')
    list_filter = ('gender', 'id')


admin.site.register(Gender, GenderAdmin)


class PassionAdmin(admin.ModelAdmin):
    list_display = ('passion', 'id')
    list_filter = ('passion', 'id')


admin.site.register(Passion, PassionAdmin)


class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'id')
    list_filter = ('status', 'id')


admin.site.register(MaritalStatus, MaritalStatusAdmin)


class UserIdealMatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserIdealMatch)


class UserPassionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserPassion)


class IdealMatchAdmin(admin.ModelAdmin):
    list_display = ('idealmatch', 'id')
    list_filter = ('idealmatch', 'id')


admin.site.register(IdealMatch, IdealMatchAdmin)

# class UserInterestAdmin(admin.ModelAdmin):

#     list_display = ('interest','user')
# list_filter = ('email', 'mobile', 'name')

# User = get_user_model()
