from django.urls import path, re_path
from .views import *


urlpatterns = [
    re_path(r'^user/all/media/(?P<user_id>[0-9a-f-]+)$',
            UserMediaAPI.as_view(), name="user_media"),

    re_path(r'^user/all/video/(?P<user_id>[0-9a-f-]+)$',
            UserVideoAPI.as_view(), name="uservideo"),
    # path('user/all/media/', UserMediaAPI.as_view(), name="user-media"),
    # path('user/media/add', UserMediaAPIPost.as_view(),name="usermediaapipost"),
    path('user/media/reaction/', MediaReactionApi.as_view(), name="media-reaction"),
    # path('user/views/<int:id>', MediaViewAPI.as_view(), name='MediaViewAPI'),
    # path('user/like/<int:id>', MediaLikeAPI.as_view(), name='MediaViewAPI'),
    # path('user/share/<int:id>', MediaShareAPI.as_view(), name='MediaViewAPI'),
    path('upload/', MediaUploadApi.as_view(), name='media-upload'),
    #     path('upload/1/', MediaUploadV2Api.as_view(), name='media-upload'),

    # path('media/delete/', UserMediaDeleteApi.as_view(), name='media-delete-api'),
    re_path(r'^delete/media/(?P<media_id>[0-9a-f-]+)$',
            UserMediaDeleteApi.as_view(), name="media-delete"),
    # path('media/<int:id>', GetMediaUploadApi.as_view(), name='MediaUploadApi'),
    path('media/reports/', MediaReportsApiView.as_view(), name='media_report'),
    #
]
