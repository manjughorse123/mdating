from django.urls import path, re_path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('post/', PostUploadApi.as_view(), name='postapi'),
    path('post/<int:pk>', PostUploadApi.as_view(), name="postapi"),
    re_path(r'^user/all/image/(?P<id>[0-9a-f-]+)', UserImages.as_view(), name="userimages"),
    path('post/reaction/', PostReactionApi.as_view(), name="postreactionapi"),
    # path('post/reaction/<int:id>', PostReactionApi.as_view(), name="postreactionapi"),
    path('all/post/api', AllPostAPI.as_view(), name="allpostapi"),


    # re_path(r'^post/reaction/(?P<id>[0-9a-f-]+)', PostReactionApi.as_view(), name="postreactionapi"),
    # re_path(r'^post/(?P<id>[0-9a-f-]+)', PostUploadApi.as_view(), name="postapi"),

]
