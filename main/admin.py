from django.contrib import admin
from .models import *


# Register your models here.
class UserMediaAdmin(admin.ModelAdmin):
    list_display = ('create_at', 'media')
    list_filter = ('create_at',)


class UserInterestAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('interest',)}
    list_display = ('interest', 'create_at')
    list_filter = ('interest', 'create_at')


class UserIdeaMatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('ideamatch',)}
    list_display = ('ideamatch', 'create_at')
    list_filter = ('ideamatch', 'create_at')


class RelationshipStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('relationship_status',)}
    list_display = ('relationship_status', 'create_at')
    list_filter = ('relationship_status', 'create_at')


class EducationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('educations',)}
    list_display = ('educations', 'create_at')
    list_filter = ('educations', 'create_at')


class BodyTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('body_type',)}
    list_display = ('body_type', 'create_at')
    list_filter = ('body_type', 'create_at')


class IsVerifiedAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('is_verified',)}
    list_display = ('is_verified', 'create_at')
    list_filter = ('is_verified', 'create_at')


class GenderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('gender',)}
    list_display = ('gender', 'create_at')
    list_filter = ('gender', 'create_at')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'create_at', 'update_at')
    list_filter = ('user', 'create_at', 'update_at')


admin.site.register(UserMedia, UserMediaAdmin)
admin.site.register(UserInterest, UserInterestAdmin)
admin.site.register(UserIdeaMatch, UserIdeaMatchAdmin)
admin.site.register(RelationshipStatus, RelationshipStatusAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(BodyType, BodyTypeAdmin)
admin.site.register(IsVerified, IsVerifiedAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Profile, ProfileAdmin)


