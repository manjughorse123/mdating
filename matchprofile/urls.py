from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('user/filter/', UserFilterApiView.as_view(), name='user_filter'),

    path('user/search/filter/', UserSearchFilterApiView.as_view(),
         name='search_filter'),

    #     path('matched-profile/', MatchedUserProfileView.as_view(),
    #          name='matchprofilelikeunlike'),
    #     path('user/filter/V2/', UserFilterAPIV2.as_view(), name='userfilter'),
    #     path('matched-profile/V2', MatchedUserProfileViewV2.as_view(),
    #     name = 'matchprofilelikeunlike'),

]
