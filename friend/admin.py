import imp
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(FriendList)
admin.site.register(FollowAccept)
admin.site.register(FollowRequest)
admin.site.register(FAQ)
