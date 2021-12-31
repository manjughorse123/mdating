from django.contrib import admin
from .models import *


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'otp', 'create_at')
    list_filter = ('mobile', 'create_at')
    # readonly_fields = ('user', 'mobile', 'otp', 'create_at')


admin.site.register(UserProfile, UserProfileAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'create_at')
    list_filter = ('email', 'create_at')
    # readonly_fields = ('email', 'name', 'create_at')


admin.site.register(User, UserAdmin)
