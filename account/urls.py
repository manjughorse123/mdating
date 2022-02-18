from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    re_path(r'^user/data/(?P<id>[0-9a-f-]+)', UserData.as_view(), name='UserData'),
    # path('user/data/', UserData.as_view(), name='UserData'),
    # re_path(r'^user/update/(?P<pk>[0-9a-f-]+)', UserUpdate.as_view(), name="userupdate"),

    # path('signup/', UserCreateView.as_view(), name='signup'),
    #Master Api Urls 
    path('passion/', AddPassionView.as_view(), name='passion_view'),
    path('gender/', AddGenderView.as_view(), name='_genderView'),
    path('merital-status/', AddMaritalStatusView.as_view(), name='merital_statusView'),
    path('ideal-match/', AddIdealMatchView.as_view(), name='ideal_matchView'),
    path('height/',  AddHeigthView.as_view(), name='heigthview'),
    # re_path('UserUpdatePassion/(?P<pk>[0-9a-f-]+)',  UserUpdatePassion.as_view({'get':'list'}), name='match_detail'),

    re_path(r'^get/user/detail/(?P<pk>[0-9a-f-]+)', GetUserDetail.as_view(), name='getuserdetail'),
    re_path(r'^user/update/ideal-match/(?P<pk>[0-9a-f-]+)', UserUpdateIdealMatch.as_view(), name="userupdateidealmatch"),
    re_path(r'^user/update/passion/(?P<pk>[0-9a-f-]+)', UserUpdatePassion.as_view(), name="userupdatepassion"),
    re_path(r'^user/update/gender/(?P<pk>[0-9a-f-]+)', UserUpdateGender.as_view(), name="userupdategender"),
    re_path(r'^user/update/interest/(?P<pk>[0-9a-f-]+)', UserUpdateInterest.as_view(), name="userupdateinterest"),
    re_path(r'^user/update/hight/(?P<pk>[0-9a-f-]+)', UserUpdateHight.as_view(), name="userupdatehight"),
    re_path(r'^user/update/location/(?P<pk>[0-9a-f-]+)', UserUpdateLoction.as_view(), name="userupdatelocation"),
    re_path(r'^user/update/relationship-status/(?P<pk>[0-9a-f-]+)', UserUpdateMaritalStatus.as_view(), name="userupdatemaritalstatus"),
    re_path(r'^user/delete/(?P<pk>[0-9a-f-]+)', UserDelete.as_view(), name="userdelete"),

]
