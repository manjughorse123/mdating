from django.urls import path
from .views import *

urlpatterns=[
    path('profilelist', ProfileList.as_view(), name="profilelist"),
]