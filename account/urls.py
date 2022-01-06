from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name="Login"),
    path('otp/verify', OTPVerify.as_view(), name='OTPVerify'),
    path('registration', Registration.as_view(), name='Registration'),
    path('user/data', UserData.as_view(), name='UserData'),
    path('user/update/<int:pk>', UserUpdate.as_view(), name="userupdate")



]
