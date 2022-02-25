from django.urls import path, re_path
from .views import *

urlpatterns = [

    # path('match-like-user/', AddMatchLikeUserProfileView.as_view(), name='match-like-user'),
    # path('like-to-like/', AddLikeToLikeView.as_view(), name='post_list_list'),
    # path('like-count/', PostCountLikeView.as_view(), name='count'),
    path('matched-profile/', MatchedUserProfileView.as_view(), name='matchprofilelikeunlike'),


]

