from django.urls import path, re_path
from .views import *
from . import views
urlpatterns = [
    path('index/',views.index),
    
    path('genderlist/',  GenderList.as_view(), name='genderlist'),
    re_path('genderedit/(?P<pk>[0-9]+)/', GenderEditView.as_view(), name='genderedit'),
    path('passionlist/', PassionList.as_view(), name='passionlist'),
    path('marital-status-list/', MaritalStatusList.as_view(), name='maritalstatuslist'),
    path('faq-list/', FAQView.as_view(), name='faqlist'),
    path('userverified-list/', UserVerifiedList.as_view(), name='userverifiedlist'),
    path('ideal-match-list/', IdealMatchProfile.as_view(), name='idealmatchlist'),
    
 
]