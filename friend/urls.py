from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('friend-request-send/',
         AddFriendRequestSendView.as_view(), name='send_request'),
    path('friend-request-accept-user/',
         AddFriendRequestAcceptDetailApiView.as_view(), name='accept_request'),
    path('get-friend-req-list/', GetFriendRequestListApiView.as_view(),
         name="get_friend_req_list"),
    path('get-friend-req-accept-list/v2/', GetFriendRequestAcceptApiViewV2.as_view(),
         name="get_friend_req_list"),
    re_path(r'^user-friends-list/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptApiView.as_view(), name="get_friend_req_list"),
    path('send-req-by-user/', SendRequestByUserApiView.as_view(),
         name="send_req_by_user"),

#     path('send-follow-request/',
#          AddFollowRequestView.as_view(), name='follow_request'),
    path('follow-send-accept/',
         FollowRequestAcceptView.as_view(), name='follow_accept'),
    re_path(r'^get-following/(?P<user_id>[0-9a-f-]+)$',
            GetFollowingApiView.as_view(), name="get_following"),
    re_path(r'^get-follower/(?P<user_id>[0-9a-f-]+)$',
            GetFollowerApiView.as_view(), name="get_follower"),

    path('follow-request/', SendFollowRequestView.as_view(),
         name='send_follow_request'),
#     path('follow-back-accept/', SendFollowRequestView.as_view(), name='follow_back'),
    path('follow-back-accept/', FollowBackApiView.as_view(), name='follow_back'),#change for testing follow 7 oct 
    path('get-follow-back/', GetFollowBackApiView.as_view(), name='getfollowback'),



    path('test-follow-suggested/', TestingSuggestedFollowApiView.as_view(),
         name='test_get_followback'),
    re_path(r'^user-friends-list/testing/(?P<user_id>[0-9a-f-]+)$',
            GetFriendRequestAcceptViewTesting.as_view(), name="get_friend_req_list_test"),

    path('get-friend-suggested-list/', GetFriendSuggestedListApiView.as_view(),
         name="get_friend_suggested_list"),
     
     re_path(r'^get-follower-suggestion/(?P<user_id>[0-9a-f-]+)/$',
            GetFollowerSuggestionApiView.as_view(), name="get_follower_suggestion"),

]
