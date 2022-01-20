from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    path('signup/', UserCreateView.as_view(), name='SignUP'),
    
    path('user/data', UserData.as_view(), name='UserData'),
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
    
]
