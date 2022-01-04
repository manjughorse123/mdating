from django.shortcuts import render, get_object_or_404
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random


# Create your views here.

class ProfileList(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# User Gender API Data
class GenderList(ListAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class GenderCreate(ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class GenderUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


# User Interest Api Data
class UserInterestList(ListAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


class UserInterestCreate(ListCreateAPIView):
    QuerySet = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


class UserInterestUpdate(RetrieveUpdateDestroyAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


# Ideal Match API Data
class UserIdeaMatchList(ListAPIView):
    queryset = UserIdeaMatch.objects.all()
    serializer_class = UserIdeaMatchSerializer


class UserIdeaMatchCreate(ListCreateAPIView):
    queryset = UserIdeaMatch.objects.all()
    serializer_class = UserIdeaMatchSerializer


class UserIdeaMatchUpdate(RetrieveUpdateDestroyAPIView):
    queryset = UserIdeaMatch.objects.all()
    serializer_class = UserIdeaMatchSerializer


# Relationship Status API Data
class RelationshipStatusList(ListAPIView):
    queryset = RelationshipStatus.objects.all()
    serializer_class = RelationshipStatusSerializer


class RelationshipStatusCreate(ListCreateAPIView):
    queryset = RelationshipStatus.objects.all()
    serializer_class = RelationshipStatusSerializer


class RelationshipStatusUpdate(RetrieveUpdateDestroyAPIView):
    queryset = RelationshipStatus.objects.all()
    serializer_class = RelationshipStatusSerializer
