from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path('user-like/',  UserLikeView.as_view(), name='user-like'),
    #
    # path('user-like-new/',  UserLikeNewView.as_view(), name='user-like-new'),
    # re_path(r'^get-user-like-view/(?P<pk>[0-9a-f-]+)$/', GetUserLikeView.as_view(), name="userlike"),
    # re_path(r'^get-following/(?P<pk>[0-9a-f-]+)$', GetFollowingView.as_view(), name="userupdate"),
    # re_path(r'^match-user-profile/(?P<pk>[0-9a-f-]+)$', MatchUserProfileView.as_view(), name="match_detail"),
    # path('match-user-profile/',  MatchUserProfileView.as_view(), name='match_detail'),
]