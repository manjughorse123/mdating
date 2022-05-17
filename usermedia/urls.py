from django.urls import path, re_path
from usermedia.views import *


urlpatterns = [
    re_path(r'^user/all/media/(?P<user_id>[0-9a-f-]+)$',
            UserMediaApiView.as_view(), name="user_media"),
    re_path(r'^user/all/video/(?P<user_id>[0-9a-f-]+)$',
            UserVideoApiView.as_view(), name="user_video"),
    path('user/media/reaction/',
         MediaReactionApiView.as_view(), name="media_reaction"),
    path('upload/', MediaUploadApiView.as_view(), name='media_upload'),
    re_path(r'^delete/media/(?P<media_id>[0-9a-f-]+)$',
            UserMediaDeleteApiView.as_view(), name="media-delete"),
    path('media/reports/', MediaReportsApiView.as_view(), name='media_report'),



    # path('user/all/media/', UserMediaAPI.as_view(), name="user-media"),
    # path('user/media/add', UserMediaAPIPost.as_view(),name="usermediaapipost"),
    # path('media/<int:id>', GetMediaUploadApi.as_view(), name='MediaUploadApi'),
    # path('upload/1/', MediaUploadV2Api.as_view(), name='media-upload'),
    # path('user/views/<int:id>', MediaViewAPI.as_view(), name='MediaViewAPI'),
    # path('user/like/<int:id>', MediaLikeAPI.as_view(), name='MediaViewAPI'),
    # path('user/share/<int:id>', MediaShareAPI.as_view(), name='MediaViewAPI'),
    # path('media/delete/', UserMediaDeleteApi.as_view(), name='media-delete-api'),
]
