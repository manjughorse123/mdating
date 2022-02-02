# from django.conf.urls import url
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('userfilter/', UserFilterAPI.as_view(), name='userfilter'),
    path('data/userfilter/', UserPassionFilterAPI.as_view(), name='userpassionfilter'),
    # path('userdate/', BirthDateFilter.as_view(), name='userdate'),
    path('follow/detail', FollowDetails.as_view(), name='followdetails'),
    re_path(r'^follow/request/(?P<id>[0-9a-f-]+)/flag=(?P<flag>[0-9a-f-]+)', FollowResquestAPI.as_view(), name="followresquestapi"),

    # path('UserMatchProfileFilterAPI', UserMatchProfileFilterAPI.as_view(), name='UserMatchProfileFilterAPI'),
    # path('UserPassionFilterAPI', UserPassionFilterAPI.as_view(), name='UserPassionFilterAPI')
    # path('follow/request/<int:pk>/', FollowResquestAPI.as_view(), name="followresquestapi"),
    path('UserMatchProfile', UserMatchProfileFilterAPI.as_view(), name='UserMatchProfile')
]
