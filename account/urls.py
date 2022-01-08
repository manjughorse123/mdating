from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    path('user/data', UserData.as_view(), name='UserData'),
    re_path(r'^user/update/(?P<pk>[0-9a-f-]+)', UserUpdate.as_view(), name="userupdate")
]
