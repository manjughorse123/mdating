from django.contrib import admin

# Register your models here.
from .models import *


class PostUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'message', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostUpload, PostUploadAdmin)


class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostReaction, PostReactionAdmin)


class MediaPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'id', 'is_view', 'is_like', 'is_share', 'create_at')
    list_filter = ('create_at', 'user')


admin.site.register(MediaPost, MediaPostAdmin)


class MediaReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(MediaReaction, MediaReactionAdmin)
