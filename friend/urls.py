from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('friend-request-send/',
         AddFriendRequestSendView.as_view(), name='send_request'),
    path('friend-request-accept-user/',
         AddFriendRequestAcceptDeatilApiView.as_view(), name='accept_request'),
    path('get-friend-req-list/', GetFriendRequestListApiView.as_view(),
         name="get_friend_req_list"),
    path('get-friend-req-accept-list/v2/', GetFriendRequestAcceptApiViewV2.as_view(),
         name="get_friend_req_list"),
    re_path(r'^user-friends-list/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptApiView.as_view(), name="get_friend_req_list"),
    path('send-req-by-user/', SendRequestByUserApiView.as_view(),
         name="send_req_by_user"),

    path('send-follow-request/',
         AddFollowRequestView.as_view(), name='follow_request'),
    path('follow-send-accept/',
         FollowRequestAcceptView.as_view(), name='follow_accept'),
    re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$',
            GetFollowingApiView.as_view(), name="get_following"),
    re_path(r'^get-follower/(?P<user_id>[0-9a-f-]+)$',
            GetFollowerApiView.as_view(), name="get_follower"),

    path('follow-request/', SendFollowRequestView.as_view(),
         name='send_follow_request'),
    path('follow-back-accept/', FollowBackApiView.as_view(), name='follow_back'),
    path('get-follow-back/', GetFollowBackApiView.as_view(), name='getfollowback'),



    path('test-follow-suggested/', TestingSuggestedFollowApiView.as_view(),
         name='test_get_followback'),
    re_path(r'^user-friends-list/testing/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptViewTesting.as_view(), name="get_friend_req_list_test"),

    #     re_path(r'^get-user-follower/(?P<user_id>[0-9a-f-]+)$',
    #             GetFollowersView.as_view(), name="getfollower"),
    # re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$', GetFollowingView.as_view(), name="userfollownew"),

    # path('faq/', FAQView.as_view(), name='question'),
    # re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$',
    #         GetFollowerFollowingView.as_view(), name="get-following"),
    #     path('get-follower/', GetFollowerV2View.as_view(), name="getfollower"),
    # re_path(r'^get-friend-req-list/(?P<user_id>[0-9a-f-]+)$',
    #         GetFriendRequestListView.as_view(), name="get_friend_req_list"),
    # path('friend-request-accept/', AddFriendRequestAcceptView.as_view(), name='accept'),
    #     path('get-following/', GetFollowerV3View.as_view(), name="getfollowing"),

]
