from django.urls import path, re_path
from .views import *



urlpatterns=[

    path('user-verification/',UserVerificationView.as_view(), name='user_verification'),
    path('admin-user-verified/', AdminUserVerifiedView.as_view(), name='admin-user-verified'),

  

]