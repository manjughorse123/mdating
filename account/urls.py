from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
    path('login/', LoginApiView.as_view(), name="login"),
    path('otp/verify/', OTPVerifyApiView.as_view(), name='otp_verify'),
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    re_path(r'user/data/(?P<user_id>[0-9a-f-]+)$',
            UserDataApiView.as_view(), name='profile_timeline'),
    re_path(r'^user/update/profile/(?P<user_id>[0-9a-f-]+)$',
            UserUpdateProfileApiView.as_view(), name="userupdate"),
    path('user/update/profile/v2/',
         UserUpdateProfileV2.as_view(), name="userprofileupdate"),
    path('get/user/detail/', GetUserDetailApiView.as_view(),
         name='user-detail'),  # GetUserDetailV2 v2version
    path('user/verified/', UserVerifiedApiView.as_view(), name='user-verify'),
    path('user/verify/doc/', UserVerifyDocumentApi.as_view(), name='user-verify'),
    path('resend-otp/', ResendOtpApiView.as_view(),
         name='resend_otp'),  # resend api
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('setting/privacy/', SettingPrivacyApiView.as_view(), name='setting-privacy'),

    # path('otp/verify/v2', OTPVerifyV2.as_view(), name='OTPVerify'),# OTPVerifyV2 for Jwt Token checking
    # re_path(r'^user/verified/(?P<user_id>[0-9a-f-]+)$', UserVerifiedAPI.as_view(), name='user-verification'),
    #     re_path(r'^get/user/detail/(?P<user_id>[0-9a-f-]+)$',
    #             GetUserDetail.as_view(), name='getuserdetail'),
    # re_path(r'^user/Delete/(?P<user_id>[0-9a-f-]+)$', UserDelete.as_view(), name="userdelete"),
    #     path('user/data/new/', UserDataV2.as_view(), name='UserData'),
    # path('signup/', UserCreateView.as_view(), name='signup'),
    #     path('user/edit/', UserProfileMediaEditAPI.as_view(), name="useredit"),
]
