from django.urls import path
from .views import *

urlpatterns = [
    path('LoginAttempt', LoginAttempt.as_view(), name="LoginAttempt"),
    path('LoginOtp', LoginOtp.as_view(), name='LoginOtp'),
    path('VirifyOtp', VirifyOtp.as_view(), name='VirifyOtp'),
    path('Registration', Registration.as_view(), name='Registration'),

]
