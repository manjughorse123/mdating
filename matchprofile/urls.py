from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('user/filter/', UserFilterAPI.as_view(), name='userfilter'),
    path('matched-profile/', MatchedUserProfileView.as_view(), name='matchprofilelikeunlike'),


]

