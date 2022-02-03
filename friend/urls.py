from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('friend-request-send/', AddFriendRequestSendView.as_view(), name='send_request'),
    path('friend-request-accept/', AddFriendRequestAcceptView.as_view(), name='accept'),
    re_path(r'^get-friend-req-list/(?P<pk>[0-9a-f-]+)', GetFriendRequestListView.as_view(), name="get_friend_req_list"),
    path('follow-request/', AddFollowRequestView.as_view(), name='followRequest'),
    path('follow-accept/', FollowRequestAcceptView.as_view(), name='follow_accept'),
    re_path(r'^get-follower/(?P<pk>[0-9a-f-]+)', GetFollowerView.as_view(), name="userupdate"),
    re_path(r'^get-following/(?P<pk>[0-9a-f-]+)', GetFollowingView.as_view(), name="userupdate"),
    path('faq/', FAQView.as_view(), name='question'),
    path('faq-detail/<int:pk>/', FAQDetailUpdateInfoView.as_view(), name='faq_detail'),



]