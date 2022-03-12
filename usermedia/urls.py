from django.urls import path, re_path
from .views import *


urlpatterns = [
    # re_path(r'^user/all/media/(?P<user_id>[0-9a-f-]+)$', UserMediaAPI.as_view(), name="usermediaapi"),
    # path('user/media/add', UserMediaAPIPost.as_view(),name="usermediaapipost"),
    # path('user/media/reaction', MediaReactionApi.as_view(),name="mediareactionapi"),
    # path('user/views/<int:id>', MediaViewAPI.as_view(), name='MediaViewAPI'),
    # path('user/like/<int:id>', MediaLikeAPI.as_view(), name='MediaViewAPI'),
    # path('user/share/<int:id>', MediaShareAPI.as_view(), name='MediaViewAPI'),
    path('upload/', MediaUploadApi.as_view(), name='MediaUploadApi'),
    # path('media/<int:id>', GetMediaUploadApi.as_view(), name='MediaUploadApi'),
]