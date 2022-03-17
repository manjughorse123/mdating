import json
from datetime import date
from django.utils.timezone import now
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

from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

 

class UserFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()

    # def age_range(min_age, max_age):
    #     current = now().date()
    #     min_date = date(current.year - min_age, current.month, current.day)
    #     max_date = date(current.year - max_age, current.month, current.day)
    #
    #     return User.objects.filter(birth_date__gte=max_date,
    #                                 birth_date__lte=min_date).order_by("birth_date")

    class Meta:
        model = User
        fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range']}


class UserPassionFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()
    # age_range = django_filters.CharFilter(
    #     field_name='calculate_age')

    class Meta:
        model = User
        # fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], 'passion': ['exact'], 'idealmatch':['exact']}
        fields = {'gender': ['exact'], 'birth_date': ['exact', 'range'], 'passion': ['exact'],
                  'idealmatch': ['exact']}
        # fields = ('age_range','gender','passion',)

class UserFilterAPI(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserPassionFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)


    # def get_queryset(self):
    #     print ("request",self.request.user)
    #     return self.request.account.users.all()
    def get_queryset(self):

        if 'min_age'  in self.request.GET:
            min_age = self.request.GET['min_age']
            current = now().date()
            min_date = date(current.year - int(min_age), current.month, current.day)

        if 'max_age'  in self.request.GET:
            max_age = self.request.GET['max_age']
            current = now().date()
            max_date = date(current.year - int(max_age), current.month, current.day)
        # current = now().date()
        # min_date = date(current.year - int(min_age), current.month, current.day)
        # max_date = date(current.year - int(max_age), current.month, current.day)

            return User.objects.filter(birth_date__gte=max_date,
                                       birth_date__lte=min_date).order_by("birth_date")

    @swagger_auto_schema(

        operation_summary="Get user Filter by Location,Passion,Gender ",

        tags=['User Filter']

    )
    def get(self, request, *args, **kwargs):

        response = super(UserFilterAPI, self).get(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
        return response



class UserFilterAPIV2(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)
    #
    @swagger_auto_schema(

        operation_summary = "Get user Filter by Location,Passion,Gender ",

        tags = ['User Filter']
    )

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserFilterSerializer(queryset, many=True)
    #     return Response({"message": "User Matched Profile","status": 200, "success": True,'data': serializer.data},status= status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):

        response = super(UserFilterAPI, self).get(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
        return response

class FollowDetails(GenericAPIView):
    serilaizer_class = (FollowRequestSerializer)
    def post(self, request, *args, **kwargs):
        data = {
            'user': request.data.get('user'),
        }
        flag = request.POST.get('flag')
        flagdata = int(flag)
        serializerRequest = FollowRequestSerializer(data=request.data)
        serializerAccept = FollowAcceptSerializer(data=request.data)
        return Response({"message": "User Matched Profile","status": 200, "success": True},status=status.HTTP_200_OK)


class FollowResquestAPI(APIView):
    def get(self, request, id, flag, *args, **kwargs):

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
    @swagger_auto_schema(
      
        operation_summary = "Get Match Profile Api",
      
        tags = ['Match Profile']
    )

    def get(self, request):
        queryset = NewUserMatchProfile.objects.all()
        serializer = UserMatchProfileFilter(queryset, many=True)
        return Response({"message": "User Matched Profile", "status": 200, "success": True, 'data': serializer.data},
                        status=status.HTTP_200_OK)


# class UserPassionFilter(filters.FilterSet):
#     birth_date = DateFromToRangeFilter()
#     class Meta:
#         model = User
#         fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], 'passion': ['exact'], 'idealmatch':['exact']}
# 

class UserPassionFilterAPI(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserPassionFilter
    filter_backends = (
         DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)
# DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter,