from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
    path('login/', Login.as_view(), name="Login"),
    path('otp/verify/', OTPVerify.as_view(), name='OTPVerify'),
    # path('otp/verify/v2', OTPVerifyV2.as_view(), name='OTPVerify'),# OTPVerifyV2 for Jwt Token checking

    path('registration/', Registration.as_view(), name='Registration'),
    # re_path(r'user/data/(?P<user_id>[0-9a-f-]+)$', UserData.as_view(), name='UserData'),
    path('user/data/', UserData.as_view(), name='UserData'),
    # re_path(r'^user/update/profile/(?P<user_id>[0-9a-f-]+)$', UserUpdateProfile.as_view(), name="userupdate"),
    path('user/update/profile/', UserUpdateProfile.as_view(), name="userprofileupdate"),
    # path('signup/', UserCreateView.as_view(), name='signup'),
    path('user/edit/', UserProfileMediaEditAPI.as_view(), name="useredit"),
    # re_path(r'^get/user/detail/(?P<user_id>[0-9a-f-]+)$', GetUserDetail.as_view(), name='getuserdetail'),
    path('get/user/detail/', GetUserDetailV2.as_view(), name='user-detail'),# GetUserDetailV2 v2version

    # re_path(r'^user/Delete/(?P<user_id>[0-9a-f-]+)$', UserDelete.as_view(), name="userdelete"),
    # path('user/verified/', UserVerifiedApi.as_view(), name='logoutapi'),
    re_path(r'^user/verified/(?P<user_id>[0-9a-f-]+)$', UserVerifiedAPI.as_view(), name='user-verification'),


    path('logout/', LogoutApiView.as_view(), name='logoutapi'),#logout api

]
