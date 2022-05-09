from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('friend-request-send/',
         AddFriendRequestSendView.as_view(), name='send_request'),
    # path('friend-request-accept/', AddFriendRequestAcceptView.as_view(), name='accept'),
    path('friend-request-accept-user/',
         AddFriendRequestAcceptDeatilApiView.as_view(), name='accept'),
    path('get-friend-req-list/', GetFriendRequestListViewV2.as_view(),
         name="get_friend_req_list"),
    # re_path(r'^get-friend-req-list/(?P<user_id>[0-9a-f-]+)$',
    #         GetFriendRequestListView.as_view(), name="get_friend_req_list"),
    path('get-friend-req-accept-list/v2/', GetFriendRequestAcceptViewV2.as_view(),
         name="get_friend_req_list"),
    re_path(r'^user-friends-list/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptView.as_view(), name="get_friend_req_list"),
    path('send-follow-request/',
         AddFollowRequestView.as_view(), name='followRequest'),
    path('follow-send-accept/',
         FollowRequestAcceptView.as_view(), name='follow_accept'),
    #     path('get-following/', GetFollowerV3View.as_view(), name="getfollowing"),
    re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$',
            GetFollowerV3View.as_view(), name="get-following"),
    # re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$',
    #         GetFollowerFollowingView.as_view(), name="get-following"),
    #     path('get-follower/', GetFollowerV2View.as_view(), name="getfollower"),
    re_path(r'^get-follower/(?P<user_id>[0-9a-f-]+)$',
            GetFollowerV2View.as_view(), name="getfollower"),
    #     re_path(r'^get-user-follower/(?P<user_id>[0-9a-f-]+)$',
    #             GetFollowersView.as_view(), name="getfollower"),
    # re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$', GetFollowingView.as_view(), name="userfollownew"),

    # path('faq/', FAQView.as_view(), name='question'),
    path('send-req-by-user/', SendRequestByUser.as_view(), name="send_req_by_user"),

    path('follow-request/', SendFollowRequestView.as_view(),
         name='sendfollowRequest'),
    path('follow-back-accept/', FollowBackApiView.as_view(), name='followback'),
    path('get-follow-back/', GetFollowBackApiView.as_view(), name='getfollowback'),
    path('test-follow-suggested/', TestingSuggestedFollowApiView.as_view(),
         name='testinggetfollowback'),

    re_path(r'^user-friends-list/testing/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptViewTesting.as_view(), name="get_friend_req_list"),



]
