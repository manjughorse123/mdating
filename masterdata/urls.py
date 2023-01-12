from django.urls import path, re_path
from .views import *


urlpatterns = [

     path('get-public-privacy/',index),
     path('term-and-condition/',termAndConditionView,name="term-and-condition"),
      path('faq-detail/',faqHtmlView,name="faq-data"),
    #  term-and-condition
    
    path('faq/', FAQView.as_view(), name='question'),
    path('get-master-data/', GetMasterData.as_view(), name='getmasterdata'),

    path('get-notification/', AddNotificationData.as_view(), name='get-notification'),
    path('term-condition/', TermAndConditionView.as_view(), name='term-and-condition'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    
    # path('get-master-data/v2', GetMasterDataV2.as_view(), name='getmasterdata'),
]
