import json

import django_filters
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_gis.filters import InBBoxFilter, TMSTileFilter
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_gis.filters import DistanceToPointOrderingFilter
from django_filters import rest_framework as filters, IsoDateTimeFilter, DurationFilter, DateFromToRangeFilter, \
    MultipleChoiceFilter, TypedChoiceFilter, ModelChoiceFilter, RangeFilter, ModelMultipleChoiceFilter, CharFilter
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from matchprofile.models import *


class UserFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()

    class Meta:
        model = User
        fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], }


class UserFilterAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)


# DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter

# class BirthDateFilter(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserFilterSerializer
#     filterset_class = UserFilter
#     distance_filter_field = 'geometry'
#
#     filter_backends = [DjangoFilterBackend, TMSTileFilter, OrderingFilter, SearchFilter]


class FollowDetails(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'user': request.data.get('user'),
        }
        flag = request.POST.get('flag')
        flagdata = int(flag)
        serializerRequest = FollowRequestSerializer(data=request.data)
        serializerAccept = FollowAcceptSerializer(data=request.data)
        return Response(status=status.HTTP_200_OK)


class FollowResquestAPI(APIView):
    def get(self, request, id, flag, *args, **kwargs):
        # import pdb;pdb.set_trace()
        # flag = kwargs.get(flag)
        # print("sjkdhkj", flag)
        # import pdb;pdb.set_trace()
        # flag = request..get("1")
        # flag = "1"
        data = int(flag)
        if data == 1:
            follow = FollowRequest.objects.filter(user_id=id)
            serializer = FollowRequestSerializer(follow, many=True)
            return Response({"message": "Follow Request", "status": 200,"success": "True", "user": [serializer.data]},
                            status=status.HTTP_200_OK)
        if data == 2:
            follow = FollowAccept.objects.filter(user_id=id)
            serializer = FollowAcceptSerializer(follow, many=True)
            return Response({"message": "Follow Accept", "status": 200,"success": "True", "user": [serializer.data]},
                            status=status.HTTP_200_OK)


#
# class IdealMatchFilter(filters.FilterSet):
#     idealmatch = ModelChoiceFilter()
#     class Meta:
#         model = UserIdealMatch
#         fields = ['idealmatch']
#         # fields = {'idealmatch': ['MultipleChoiceFilter'], }
#
#
# class IdealMatchFilterAPI(ListAPIView):
#     queryset = UserIdealMatch.objects.all()
#     serializer_class = UserIdealMatchSerializer
#     filterset_class = IdealMatchFilter
#     filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
#
#
# class UserPassionFilter(filters.FilterSet):
#     class Meta:
#         model = UserPassion
#         fields = ('passion',)
#
#
# class UserPassionFilterAPI(ListAPIView):
#     queryset = UserPassion.objects.all()
#     serializer_class = UserPassionSerializer
#     filterset_class = UserPassionFilter
#     filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)


class UserMatchProfileFilter(filters.FilterSet):
    user__user__name = CharFilter(field_name='id')

    class Meta:
        model = NewUserMatchProfile
        fields = ['user', 'like_profile_user']
        # fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], }


class UserMatchProfileFilterAPI(ListAPIView):
    queryset = NewUserMatchProfile.objects.all()
    serializer_class = NewUserMatchProfileFilterSerializer
    filterset_class = UserMatchProfileFilter
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)


class UserPassionFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()
    class Meta:
        model = User
        fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], 'passion': ['exact'], 'idealmatch':['exact']}


class UserPassionFilterAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserPassionFilter
    filter_backends = (
         DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)
# DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter,