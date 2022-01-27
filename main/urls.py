# from django.conf.urls import url
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('userfilter/', UserFilterAPI.as_view(), name='userfilter'),
    # path('userdate/', BirthDateFilter.as_view(), name='userdate'),
]
