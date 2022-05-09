from django.contrib import admin

# Register your models here.
from .models import *


class PostUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'message',  'id', 'create_at')
    list_display_links = ('user', 'id')
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


class NewPostUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'id', 'create_at')
    list_filter = ('create_at',)


# admin.site.register(UserPost, NewPostUserAdmin)
# admin.site.register(UserPostLike)

class PostReportAdmin(admin.ModelAdmin):
    list_display = ('post', 'id', 'report_text', 'create_at')
    list_filter = ('create_at',)


admin.site.register(PostReport, PostReportAdmin)
