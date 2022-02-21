from django.urls import path, re_path
from .views import *

urlpatterns = [

  
    path('faq/', FAQView.as_view(), name='question'),
]