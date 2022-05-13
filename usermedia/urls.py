from django.urls import path, re_path
from usermedia.views import *


urlpatterns = [
    re_path(r'^user/all/media/(?P<user_id>[0-9a-f-]+)$',
            UserMediaAPI.as_view(), name="user_media"),
    re_path(r'^user/all/video/(?P<user_id>[0-9a-f-]+)$',
            UserVideoAPI.as_view(), name="uservideo"),
    path('user/media/reaction/', MediaReactionApi.as_view(), name="media-reaction"),
    path('upload/', MediaUploadApi.as_view(), name='media-upload'),
    re_path(r'^delete/media/(?P<media_id>[0-9a-f-]+)$',
            UserMediaDeleteApi.as_view(), name="media-delete"),
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
