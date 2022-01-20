from django.urls import path, re_path
from .views import *



urlpatterns=[

    path('post_update_user/', AddPostUserUpdateView.as_view(), name='post_update'),
    path('react_count/', PostUserReactSerializerView.as_view(), name='accept'),
    path('match_user_profile/', MatchProfileUserViewSet.as_view({'get': 'list'}), name='accept_saj'),
    
]