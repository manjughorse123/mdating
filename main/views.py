import django_filters
from django.db.models import F
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
from django_filters import rest_framework as filters, IsoDateTimeFilter, DurationFilter, DateFromToRangeFilter
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()
    # birth_date = DateFromToRangeFilter

    class Meta:
        model = User
        fields = {'id': ['exact'], 'gender': ['exact'], 'birth_date': ['exact', 'range'], }


class UserFilterAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    # filterset_fields = ('name', 'address')
    filterset_class = UserFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter,DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)
# DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter

# class BirthDateFilter(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserFilterSerializer
#     filterset_class = UserFilter
#     distance_filter_field = 'geometry'
#
#     filter_backends = [DjangoFilterBackend, TMSTileFilter, OrderingFilter, SearchFilter]
