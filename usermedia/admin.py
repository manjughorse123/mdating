from django.contrib import admin
from .models import *
# Register your models here.

class MediaPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'id', 'like_count', 'create_at')
    list_filter = ('create_at', 'user')

admin.site.register(MediaPost, MediaPostAdmin)

class MediaViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(MediaView, MediaViewAdmin)


class MediaLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(MediaLike, MediaLikeAdmin)


class MediaShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_id', 'id', 'create_at')
    list_filter = ('create_at',)

admin.site.register(MediaShare, MediaShareAdmin)
