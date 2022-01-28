from django.contrib import admin

# Register your models here.
from .models import *


class PostUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'message', 'is_view', 'is_like', 'is_share', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostUpload, PostUploadAdmin)


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostLike, PostLikeAdmin)


class PostViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostView, PostViewAdmin)


class PostShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_id', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostShare, PostShareAdmin)
