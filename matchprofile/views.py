import math
from django.contrib.gis.measure import D 
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date, timedelta
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters, IsoDateTimeFilter, DurationFilter, DateFromToRangeFilter, \
    MultipleChoiceFilter, TypedChoiceFilter, ModelChoiceFilter, RangeFilter, ModelMultipleChoiceFilter, CharFilter
from DatingApp.baseurl import base_url
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_gis.filters import DistanceToPointFilter, DistanceToPointOrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.contrib.gis.db.models import *
from matchprofile.serializers import *
from matchprofile.models import *
from account.models import User
from usermedia.models import *


class UserFieldFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()

    class Meta:
        model = User
        fields = {'gender': ['exact'],
                  'birth_date': ['exact', 'range'],
                  'passion': ['exact'],
                  'idealmatch': ['exact'],
                  'marital_status': ['exact'],
                 
                  'city': ['exact']
                  }

from rest_framework import pagination
class CustomPagination(pagination.PageNumberPagination):
    
    page_query_param = "offset"   # this is the "page"
    page_size_query_param="limit" # this is the "page_size"
    page_size = 10
    max_page_size = 100
    
    def get_paginated_response(self, data1):
        return Response({
           
            'results': data1,"success": True,
             "message": "User Post by User ", "status": 200,'base_url':base_url},
        status=status.HTTP_200_OK)

class UserFilterApiView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserFieldFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        
        user_id = self.request.user.id
        user_info = User.objects.filter(id=user_id)

        today = date.today()
        last_week = today - timedelta(days=5)
        longitude = self.request.GET['longitude']
        latitude = self.request.GET['latitude']
        if  int(self.request.GET['related_distance']) > 0:
            related_distance = self.request.GET['related_distance']
        else :
            related_distance = 10000
        user_location = Point(float(latitude), float(longitude), srid=4326)
        if 'min_age' in self.request.GET:
            min_age = self.request.GET['min_age']
            current = now().date()
            min_date = date(current.year - int(min_age),
                            current.month, current.day)

        if 'max_age' in self.request.GET:
            max_age = self.request.GET['max_age']
            current = now().date()
            max_date = date(current.year - int(max_age),
                            current.month, current.day)
            
            pnt = User.objects.get(id=user_id)
            def distance_to_decimal_degrees(distance):
            
                return distance.m / 111_319.5 
            if 'interest_in' in self.request.GET:
                if len(eval(self.request.GET['interest_in'])) > 0 :
                    val = User.objects.filter(Q(is_complete_profile=True) & Q(birth_date__gte=max_date,
                                       birth_date__lte=min_date)).filter(gender__in =eval(self.request.GET['interest_in']) ,location__dwithin=(user_location, distance_to_decimal_degrees(D(km=related_distance)))).annotate(distance = Distance("location", user_location)).order_by("create_at").exclude(id=user_info[0].id).distinct()
                else :
                    val = User.objects.filter(Q(passion__in=user_info[0].passion.all()) & Q(interest_in=user_info[0].gender) & Q(is_complete_profile=True) & Q(birth_date__gte=max_date,
                                       birth_date__lte=min_date)).filter(location__dwithin=(user_location, distance_to_decimal_degrees(D(km=related_distance)))).annotate(distance = Distance("location", user_location)).order_by("create_at").exclude(id=user_info[0].id).distinct()
            
            else :
                val = User.objects.filter(Q(passion__in=user_info[0].passion.all()) & Q(interest_in=user_info[0].gender) & Q(is_complete_profile=True) & Q(birth_date__gte=max_date,
                                       birth_date__lte=min_date)).filter(location__dwithin=(user_location, distance_to_decimal_degrees(D(km=related_distance)))).annotate(distance = Distance("location", user_location)).order_by("create_at").exclude(id=user_info[0].id).distinct()
              
            return val
            
        user_data = User.objects.filter(Q(is_complete_profile=True) & Q(birth_date__year__gte=(
            user_info[0].birth_date.year - 10))
            & Q(birth_date__year__lte=(
                user_info[0].birth_date.year + 10)) &
            # Q(gender__in=user_info[0].interest_in) |
            Q(interest_in__in=user_info[0].gender) &
            Q(city=user_info[0].city) |
            Q(location=user_info[0].location) |
            Q(passion__in=user_info[0].passion.all()) |
            Q(idealmatch__in=user_info[0].idealmatch.all()) |
            Q(marital_status=user_info[0].marital_status) |
            Q(create_at__range=(last_week, today))
            & Q(is_active=False)

        ).exclude(id=user_info[0].id).order_by("create_at").distinct()
        return user_data

    @swagger_auto_schema(

        operation_summary="Get user Filter by Location,Passion,Gender,marital status ",
        tags=['User Filter']

    )
    def get(self, request, *args, **kwargs):

        response = super(UserFilterApiView, self).get(request, *args, **kwargs)
        # print("response", response.data['features'])

        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
        response.data['base_url'] = base_url

        return response


class UserFilterAPIV2(ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserFilterSerializer
    distance_filter_field = 'location'
    filterset_class = UserFieldFilter
    filter_backends = (
        DistanceToPointFilter, SearchFilter, DistanceToPointOrderingFilter, DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):

        if 'min_age' in self.request.GET:
            min_age = self.request.GET['min_age']
            current = now().date()
            min_date = date(current.year - int(min_age),
                            current.month, current.day)

        if 'max_age' in self.request.GET:
            max_age = self.request.GET['max_age']
            current = now().date()
            max_date = date(current.year - int(max_age),
                            current.month, current.day)

            return User.objects.filter(birth_date__gte=max_date,
                                       birth_date__lte=min_date).order_by("birth_date")

    @swagger_auto_schema(

        operation_summary="Get user Filter by Location,Passion,Gender ",
        tags=['User Filter']
    )
    def get(self, request, *args, **kwargs):

        response = super(UserFilterApiView, self).get(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
        return response


class UserSearchFilterApiView(ListAPIView):
    serializer_class = UserSeachFilterSerializer
    permission_classes = [IsAuthenticated, ]
    page_size = 2

  

    def get(self, request,  format=None):
        page_size = 10
        user_id = request.user.id
        # user_info = User.objects.filter(id=user_id)
        user_info = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id= %s", [user_id])
        # print("dffweasfewffgwefwe", people[0].name, people[0].age)
        user_passion = []
        # user_spe_data = User.objects.raw(
        #     "SELECT *, date_part('year', age(birth_date))::int as age  FROM account_user where city= %s  or passion= %s or idealmatch= %s ",
        #     [user_info[0].city,  user_info[0].passion, user_info[0].idealmatch])

        # for i in range(len(user_spe_data)):
        #     print("user_spe_data", user_spe_data[i], user_spe_data[i].age)
        today = date.today()
        last_week = today - timedelta(days=5)

        min_age = 18
        current = now().date()
        min_date = date(current.year - int(min_age),
                        current.month, current.day)

        max_age = 65
        current = now().date()
        max_date = date(current.year - int(max_age),
                        current.month, current.day)

        new_data = User.objects.filter(
            Q(gender=user_info[0].gender) |
            Q(city=user_info[0].city) |
            Q(location=user_info[0].location) |
            Q(passion__in=user_info[0].passion.all()) |
            Q(idealmatch__in=user_info[0].idealmatch.all()) |
            Q(marital_status=user_info[0].marital_status) |
            Q(create_at__range=(last_week, today))
            and Q(is_complete_profile=True)
        ).exclude(id=user_info[0].id).distinct()
        # new_data = User.objects.filter(Q(birth_date__year__gte=(
        #     user_info[0].birth_date.year - 10)) and Q(birth_date__year__lte=(
        #         user_info[0].birth_date.year + 10))).exclude(id=user_info[0].id).distinct()

        dat = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(new_data, request)
        # result_pages = paginator.paginate_queryset(user_spe_data, request)
        serializer = UserSeachFilterSerializer(result_page, context={
            'request': request}, many=True)
        # serializers = UserSeachFilterSerializer(result_pages, context={
        #     'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)
        # serializer = UserSeachFilterSerializer(new_data, many=True)

        # return Response({"success": True, "status": 200, "message": "Match Profile Data", "data": serializer.data, "data_count": len(serializer.data)},
        # status = status.HTTP_200_OK)





class UserDislikeApiView(GenericAPIView):
    serializer_class = UserDisLikeProfileSerializer
    permission_classes = [IsAuthenticated, ]

    
    def post(self, request, format='json'):
        if UserDisLikeProfile.objects.filter(user=request.data['user'],profile_user=request.data['profile_user']):
            return Response({"success": "true", "message": " Already Add !", "status": 200, "data": ""}, status=status.HTTP_200_OK)
        serializer = UserDisLikeProfileSerializer(data=request.data)

        print(request.data)
        if serializer.is_valid():
            
            # profile_user = request.data['profile_user']

            # to_user = serializer.validated_data['user']
            # send_request = FriendRequest.objects.filter(friend=to_user)
            # send_request.update(friendrequestsent=False)

            serializer.save()

            return Response({"success": True, "message": "user dislike!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "user not found!", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

