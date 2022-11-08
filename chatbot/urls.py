from django.urls import path, re_path
from .views import *

urlpatterns = [
    # user Registration
   
    path('send-message/', UserSendMessageView.as_view(), name='send-message'),
    re_path(r'get-sender/(?P<send_id>[0-9a-f-]+)$',
            GetUserSenderMessageView.as_view(), name='send_message'),
    re_path(r'all-sender/(?P<send_id>[0-9a-f-]+)/(?P<receive_id>[0-9a-f-]+)$',
            GetUserSenderMessageView.as_view(), name='send_message'),
    
]
