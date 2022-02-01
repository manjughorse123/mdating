from django.urls import path, re_path
from .views import *

urlpatterns = [

# <<<<<<< HEAD
    path('match-like-user/', AddMatchLikeUserProfileView.as_view(), name='match-like-user'),
    path('like-to-like/', AddLikeToLikeView.as_view(), name='post_list_list'),
    path('like-count/', PostCountLikeView.as_view(), name='count'),

]
# =======
    ##############################################################################

# >>>>>>> b5e5b2d31123a3f0cda62178ca3edc335ec0c3d2
