from django.contrib import admin
from .models import *
# Register your models here.


class MediaPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'id', 'like_count', 'create_at')
    list_filter = ('create_at', 'user')


admin.site.register(MediaPost, MediaPostAdmin)


class MediaVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_video', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(MediaVideo, MediaVideoAdmin)


class MediaLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(MediaLike, MediaLikeAdmin)
