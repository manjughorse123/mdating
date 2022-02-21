from django.urls import path, re_path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('post/', PostUploadApi.as_view(), name='postapi'),
    path('post/<int:post_id>', GetPostUploadApi.as_view(), name="postapi"),
    re_path(r'^user/get-all-post/(?P<user_id>[0-9a-f-]+)$', UserImages.as_view(), name="userimages"),
    path('post/reaction/', PostReactionApi.as_view(), name="postreactionapi"),
    # path('post/reaction/<int:id>', PostReactionApi.as_view(), name="postreactionapi"),
    path('all/post/', AllPostAPI.as_view(), name="allpostapi"),
    # path('all/post/views/api/<int:id>', PostViewAPI.as_view(), name="postview"),
    # path('all/post/likes/api/<int:id>', PostLikeAPI.as_view(), name="postlike"),
    # path('all/post/share/api/<int:id>', PostShareAPI.as_view(), name="postshare"),

    # re_path(r'^get-post-detail/(?P<user_id>[0-9a-f-]+)$', GetPostViewdetailView.as_view(), name="get-detail-post"),
    # re_path(r'^post/reaction/(?P<id>[0-9a-f-]+)', PostReactionApi.as_view(), name="postreactionapi"),
    # re_path(r'^post/(?P<id>[0-9a-f-]+)', PostUploadApi.as_view(), name="postapi"),

]
