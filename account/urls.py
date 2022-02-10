from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    path('signup/', UserCreateView.as_view(), name='SignUP'),
    
    re_path(r'^user/data/(?P<id>[0-9a-f-]+)', UserData.as_view(), name='UserData'),
    # path('user/data/', UserData.as_view(), name='UserData'),
    re_path(r'^user/update/(?P<pk>[0-9a-f-]+)', UserUpdate.as_view(), name="userupdate"),

    #Master Api Urls 
    path('passion/', AddPassionView.as_view(), name='passion_view'),

    path('passion-detail/<int:pk>/', AddPassiondetailView.as_view(), name='passion_detail'),
    path('gender/', AddGenderView.as_view(), name='_genderView'),
    path('gender-detail/<int:pk>/', AddGenderdetailView.as_view(), name='gender_detail'),
    path('merital-status/', AddMaritalStatusView.as_view(), name='merital_statusView'),
    path('merital-status-detail/<int:pk>/', AddMaritalStatusView.as_view(), name='merital_status_detail'),
    path('ideal-match/', AddIdealMatchView.as_view(), name='ideal_matchView'),
    path('ideal-match-detail/<int:pk>/',  AddIdealMatchdetailView.as_view(), name='ideal_match_detail'),
    
    #user Fetch api 
    path('user-media/', AddUserMediaView.as_view(), name='user_mediaView'),
    path('user-media-detail/<int:pk>/', AddUserMediadetailView.as_view(), name='user_media_detail'),
    # path('user_image/', AddUserImageView.as_view(), name='user_iamge'),
    path('user-ideal-match/', AddUserIdealMatchView.as_view(), name='ideal_matchView'),
    path('user-ideal-match-detail/<int:pk>/',  AddUserIdealMatchdetailView.as_view(), name='ideal_match_detail'),
    path('user-passion/', AddUserPassionView.as_view(), name='passionView'),
    path('user-passion-detail/<int:pk>/',  AddUserPassiondetailView.as_view(), name='passion_detail'),
    
    # path('match_profile/',  MatchProfileView.as_view({'get': 'list'}), name='match_detail'),
    path('match-profile/',  MatchProfileView.as_view(), name='match_detail'),
    # re_path('UserUpdatePassion/(?P<pk>[0-9a-f-]+)',  UserUpdatePassion.as_view({'get':'list'}), name='match_detail'),
    path('height/',  AddHeigthView.as_view(), name='heigthview'),
    re_path(r'^get/user/detail/(?P<pk>[0-9a-f-]+)', GetUserDetail.as_view(), name='getuserdetail'),
    re_path(r'^user/update/ideal-match/(?P<pk>[0-9a-f-]+)', UserUpdateIdealMatch.as_view(), name="userupdateidealmatch"),
    re_path(r'^user/update/passion/(?P<pk>[0-9a-f-]+)', UserUpdatePassion.as_view(), name="userupdatepassion"),
    re_path(r'^user/update/gender/(?P<pk>[0-9a-f-]+)', UserUpdateGender.as_view(), name="userupdategender"),
    re_path(r'^user/update/interest/(?P<pk>[0-9a-f-]+)', UserUpdateInterest.as_view(), name="userupdateinterest"),
    re_path(r'^user/update/hight/(?P<pk>[0-9a-f-]+)', UserUpdateHight.as_view(), name="userupdatehight"),
    re_path(r'^user/update/location/(?P<pk>[0-9a-f-]+)', UserUpdateLoction.as_view(), name="userupdatelocation"),
    re_path(r'^user/update/media/(?P<pk>[0-9a-f-]+)', UserUpdateMedia.as_view(), name="userupdatemedia"),
    re_path(r'^user/update/relationship_status/(?P<pk>[0-9a-f-]+)', UserUpdateMaritalStatus.as_view(), name="userupdatemaritalstatus"),


]
