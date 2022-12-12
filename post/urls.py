from django.urls import path, re_path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('post/', CreatePostApiView.as_view(), name='postapi'),
    re_path(r'^user/post/(?P<user_id>[0-9a-f-]+)$',
            UserAllPostApiView.as_view(), name='postapi'),
    re_path(r'^user/posts/(?P<user_id>[0-9a-f-]+)/(?P<is_private_key>[0-9a-f-]+)$',
            UserAllPrivatePostApi.as_view(), name='postapi'),
    path('user/get-all-post/', UserImagesApiView.as_view(), name="userimages"),
    path('post/reaction/', PostReactionApiView.as_view(), name="postreactionapi"),
    re_path(r'^delete/post/(?P<post_id>[0-9a-f-]+)$',
            DeletePostApiView.as_view(), name="deletepost"),
    re_path(r'^update/post/(?P<post_id>[0-9a-f-]+)$',
            UpdatePostApiView.as_view(), name="deletepost"),
    re_path(r'^user/get-all-post/(?P<user_id>[0-9a-f-]+)$',
            UserImagesApiViewV2.as_view(), name="user_images_with_id"),
    path('post/reports/', PostReportsApiView.as_view(), name='post_report'),

         re_path(r'^update/post/image/(?P<post_id>[0-9a-f-]+)$',
            UpdatePostImageApiView.as_view(), name="upadte-post-image"),
        re_path(r'^delete/post/image/(?P<post_id>[0-9a-f-]+)$',
            DeletePostImageApiView.as_view(), name="delete-post-image"),

    #     path('new-post/', NewPostUploadApi
    #          .as_view(), name='postnew'),
    # path('post/<int:post_id>', GetPostUploadApi.as_view(), name="postapi"),
    #     path('post-image/', PostMultipleImageApi.as_view(), name='postimages'),
    # re_path(r'^user/get-all-post/v2/(?P<user_id>[0-9a-f-]+)$', UserImagesV2.as_view(), name="userimages"),

    # path('post/reaction/<int:id>', PostReactionApi.as_view(), name="postreactionapi"),

    # path('all/post/views/api/<int:id>', PostViewAPI.as_view(), name="postview"),
    # path('all/post/likes/api/<int:id>', PostLikeAPI.as_view(), name="postlike"),
    # path('all/post/share/api/<int:id>', PostShareAPI.as_view(), name="postshare"),
    # re_path(r'^get-post-detail/(?P<user_id>[0-9a-f-]+)$', GetPostViewdetailView.as_view(), name="get-detail-post"),
    # re_path(r'^get-post-detail/(?P<user_id>[0-9a-f-]+)$', GetPostViewdetailView.as_view(), name="get-detail-post"),
    # re_path(r'^post/reaction/(?P<id>[0-9a-f-]+)', PostReactionApi.as_view(), name="postreactionapi"),
    # re_path(r'^post/(?P<id>[0-9a-f-]+)', PostUploadApi.as_view(), name="postapi"),


]
