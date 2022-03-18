from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('friend-request-send/', AddFriendRequestSendView.as_view(), name='send_request'),
    # path('friend-request-accept/', AddFriendRequestAcceptView.as_view(), name='accept'),
    path('friend-request-accept-user/', AddFriendRequestAcceptDeatilApiView.as_view(), name='accept'),
    path('get-friend-req-list/', GetFriendRequestListView.as_view(), name="get_friend_req_list"),
    path('get-friend-req-accept-list/', GetFriendRequestAcceptView.as_view(),
            name="get_friend_req_list"),
    # re_path(r'^get-friend-req-accept-list/(?P<user_id>[0-9a-f-]+)$', GetFriendRequestAcceptView.as_view(), name="get_friend_req_list"),
    path('follow-request/', AddFollowRequestView.as_view(), name='followRequest'),
    path('follow-accept/', FollowRequestAcceptView.as_view(), name='follow_accept'),
    path('get-following/', GetFollowerView.as_view(), name="getfollowing"),
    path('get-follower/', GetFollowerV2View.as_view(), name="getfollower"),
    # re_path(r'^get-follower/(?P<user_id>[0-9a-f-]+)$', GetFollowerV2View.as_view(), name="getfollower"),
    # re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$', GetFollowingView.as_view(), name="userfollownew"),

    # path('faq/', FAQView.as_view(), name='question'),


]