from django.contrib import admin
from .models import *


# Register your models here.
class UserInterestAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('interest',)}
    list_display = ('interest', 'create_at')
    list_filter = ('interest', 'create_at')


admin.site.register(UserInterest, UserInterestAdmin)


class UserIdeaMatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('ideamatch',)}
    list_display = ('ideamatch', 'create_at')
    list_filter = ('ideamatch', 'create_at')


admin.site.register(UserIdeaMatch)


class UserMediaAdmin(admin.ModelAdmin):
    list_display = ('media', 'create_at')
    list_filter = ('create_at',)


admin.site.register(UserMedia)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', '')
admin.site.register(Profile)
admin.site.register(PhoneOTP)
# admin.site.register(UserManager)
