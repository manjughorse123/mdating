from django.urls import path, re_path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('post/', PostUploadApi.as_view(), name='postapi'),
    path('post/<int:pk>', PostUploadApi.as_view(), name="postapi"),
    re_path(r'^user/all/image/(?P<id>[0-9a-f-]+)', UserImages.as_view(), name="userimages"),
    re_path(r'^user/all/media/(?P<id>[0-9a-f-]+)', UserMediaAPI.as_view(), name="usermediaapi"),
    path('user/media/add', UserMediaAPIPost.as_view(),name="usermediaapipost"),
    path('user/media/reaction', MediaReactionApi.as_view(),name="mediareactionapi"),
    path('post/reaction/', PostReactionApi.as_view(), name="postreactionapi"),
    # path('post/reaction/<int:id>', PostReactionApi.as_view(), name="postreactionapi"),
    path('all/post/api', AllPostAPI.as_view(), name="allpostapi"),


    # re_path(r'^post/reaction/(?P<id>[0-9a-f-]+)', PostReactionApi.as_view(), name="postreactionapi"),
    # re_path(r'^post/(?P<id>[0-9a-f-]+)', PostUploadApi.as_view(), name="postapi"),

]
