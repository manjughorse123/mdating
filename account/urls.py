from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    path('signup/', UserCreateView.as_view(), name='SignUP'),
    
    path('user/data', UserData.as_view(), name='UserData'),
    re_path(r'^user/update/(?P<pk>[0-9a-f-]+)', UserUpdate.as_view(), name="userupdate"),
    path('_interest/', AddInterestView.as_view(), name='_interestView'),
    path('interest_detail/<int:pk>/', AddInterestdetailView.as_view(), name='interest_detail'),
    path('gender/', AddGenderView.as_view(), name='_genderView'),
    path('gender_detail/<int:pk>/', AddGenderdetailView.as_view(), name='gender_detail'),
    
    path('merital_status/', AddMaritalStatusView.as_view(), name='merital_statusView'),
    path('merital_status_detail/<int:pk>/', AddMaritalStatusView.as_view(), name='merital_status_detail'),
    path('ideal_match/', AddIdealMatchView.as_view(), name='ideal_matchView'),
    path('ideal_match_detail/<int:pk>/',  AddIdealMatchdetailView.as_view(), name='ideal_match_detail'),
  
    path('user_media/', AddUserMediaView.as_view(), name='user_mediaView'),
    path('user_media_detail/<int:pk>/', AddUserMediadetailView.as_view(), name='user_media_detail'),
    # path('user_image/', AddUserImageView.as_view(), name='user_iamge'),

]
