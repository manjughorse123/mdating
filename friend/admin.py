import imp
from django.contrib import admin
from .models import *
# Register your models here.

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ( 'receiver', 'id', 'create_at')
    list_filter = ('create_at',)
admin.site.register(FriendRequest, FriendRequestAdmin)

class FriendListAdmins(admin.ModelAdmin):
    list_display = ('user',   'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(FriendList, FriendListAdmins)

class FollowAcceptAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(FollowAccept, FollowAcceptAdmin)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ('user',   'id', 'create_at')
    list_filter = ('create_at',)
admin.site.register(FollowRequest, FollowRequestAdmin)

class FAQAdmin(admin.ModelAdmin):
    list_display = (  'id', 'create_at')
    list_filter = ('create_at',)


admin.site.register(FAQ, FAQAdmin)

