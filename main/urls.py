from django.urls import path
from .views import *

urlpatterns=[
    path('profilelist', ProfileList.as_view(), name="profilelist"),

    path("gender/list", GenderList.as_view(), name='genderlist'),
    path("gender/create", GenderCreate.as_view(), name="gendercreate"),
    path("gender/update/<int:pk>", GenderUpdate.as_view(), name='genderupdate'),

    path("user/interest/list", UserInterestList.as_view(), name="userinterestlist"),
    path("user/interest/create", UserInterestCreate.as_view(), name="userinterestcreate"),
    path("user/interest/update/<int:pk>", UserInterestUpdate.as_view(), name="userinterestupdate"),

    path("user/idea/match/list", UserIdeaMatchList.as_view(), name="userideamatchlist"),
    path("user/idea/match/create", UserIdeaMatchCreate.as_view(), name="userideamatchcreate"),
    path("user/idea/match/update/<int:pk>", UserIdeaMatchUpdate.as_view(), name="userideamatchupdate"),

    path("marital/status/list", RelationshipStatusList.as_view(), name="relationshipstatuslist"),
    path("marital/status/create", RelationshipStatusCreate.as_view(), name="relationshipstatuslist"),
    path("marital/status/update/<int:pk>", RelationshipStatusUpdate.as_view(), name="relationshipstatuslist"),
]