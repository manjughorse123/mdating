from django.urls import path, re_path
from .views import *



urlpatterns=[

    path('post-update_user/', AddPostUserUpdateView.as_view(), name='post_update'),
    path('react-count/', PostUserReactSerializerView.as_view(), name='accept'),
    path('match-user-profile/', MatchProfileUserViewSet.as_view({'get': 'list'}), name='accept_saj'),
    
]