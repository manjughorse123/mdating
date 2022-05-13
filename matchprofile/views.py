from rest_framework.pagination import PageNumberPagination
from datetime import date, timedelta
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_gis.filters import DistanceToPointFilter, DistanceToPointOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters, IsoDateTimeFilter, DurationFilter, DateFromToRangeFilter, \
    MultipleChoiceFilter, TypedChoiceFilter, ModelChoiceFilter, RangeFilter, ModelMultipleChoiceFilter, CharFilter

from matchprofile.serializers import *
from matchprofile.models import *
from account.models import *
from usermedia.models import *
from account.models import User


class UserFieldFilter(filters.FilterSet):
    birth_date = DateFromToRangeFilter()

    class Meta:
        model = User
        fields = {'gender': ['exact'], 'birth_date': ['exact', 'range'], 'passion': ['exact'],
                  'idealmatch': ['exact']}


class UserFilterAPI(ListAPIView):
    permission_classes = [IsAuthenticated, ]
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

            return User.objects.filter(Q(is_complete_profile=True) and Q(birth_date__gte=max_date,
                                       birth_date__lte=min_date)).order_by("create_at").exclude(id=user_info[0].id)
            #    | Q(create_at__range=(last_week, today)) and Q(is_complete_profile=True)

        user_data = User.objects.filter(
            Q(gender=user_info[0].interest_in) |
            Q(interest_in=user_info[0].gender) |
            Q(city=user_info[0].city) |
            Q(location=user_info[0].location) |
            Q(passion__in=user_info[0].passion.all()) |
            Q(idealmatch__in=user_info[0].idealmatch.all()) |
            Q(marital_status=user_info[0].marital_status) |
            Q(create_at__range=(last_week, today))
            | Q(is_active=False)
            and Q(is_complete_profile=True)
        ).exclude(id=user_info[0].id).distinct()

        return user_data

    @swagger_auto_schema(

        operation_summary="Get user Filter by Location,Passion,Gender ",

        tags=['User Filter']

    )
    def get(self, request, *args, **kwargs):

        response = super(UserFilterAPI, self).get(request, *args, **kwargs)
        # print("response", response.data['features'])

        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
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

        response = super(UserFilterAPI, self).get(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['message'] = 'Filtered Data!'
        response.data['success'] = True
        return response


class MatchedUserProfileView(GenericAPIView):
    serializer_class = GetUserMatchProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        userInterest = UserMatchProfile.objects.all()
        serializer = GetUserMatchProfileSerializer(userInterest, many=True)
        return Response(
            {"success": True, "status": 200,
                "message": "Match Profile Users All Data", "data": serializer.data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary="Get Match Profile Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='User Id'),
                'like_profile_user': openapi.Schema(type=openapi.TYPE_STRING, description='User liked profile id '),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Add flag 1 for like ,2 for unlike , 3 for profile dislike '),
            }),

        tags=['Match Profile']
    )
    def post(self, request, format='json'):

        serializer = UserMatchProfileSerializer(data=request.data)

        if serializer.is_valid():
            ab = serializer.validated_data['user']
            like_profile_user = serializer.validated_data['like_profile_user']
            if request.data['flag'] == '1':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user):
                    return Response({"success": "error", "status": 400, "message": "User Already like Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.create(
                        user=ab, like_profile_user=like_profile_user, is_like=True)

            if request.data['flag'] == '2':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user, is_like=False):

                    return Response({"success": "error", "status": 400, "message": "User Already Dislike Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.filter(user=ab)

                    obj.is_like = False
                    # obj.save(update_fields=("is_like",))
                    obj.update()

            if request.data['flag'] == '3':
                obj = UserMatchProfile.objects.filter(
                    like_profile_user=like_profile_user)
                obj = obj[0].id
                objs = UserMatchProfile.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True, "message": "User Dislike !", "status": 200}, status=status.HTTP_200_OK)

            # serializer.save()

            return Response({"success": True, "status": 201, "message": "Match Profile Data", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400, "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class MatchedUserProfileViewV2(GenericAPIView):
    serializer_class = GetUserMatchProfileSerializer
    permission_classes = (IsAuthenticated,)

    # def get(self, request):
    #     userInterest = UserMatchProfile.objects.all()
    #     serializer = GetUserMatchProfileSerializer(userInterest, many=True)
    #     return Response(
    #         {"success": True, "status": 200, "message": "Match Profile Users All Data", "data": serializer.data},
    #         status=status.HTTP_200_OK)
    @swagger_auto_schema(

        operation_summary="Get Match Profile Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='User Id'),
                'like_profile_user': openapi.Schema(type=openapi.TYPE_STRING, description='User liked profile id '),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Add flag 1 for like ,2 for unlike , 3 for profile dislike '),
            }),

        tags=['Match Profile']
    )
    def post(self, request, format='json'):

        serializer = UserMatchProfileSerializer(data=request.data)

        if serializer.is_valid():
            ab = serializer.validated_data['user']
            like_profile_user = serializer.validated_data['like_profile_user']
            if request.data['flag'] == '1':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user):
                    return Response({"success": "error", "status": 400, "message": "User Already like Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.create(
                        user=ab, like_profile_user=like_profile_user, is_like=True)

            if request.data['flag'] == '2':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user, is_like=False):

                    return Response({"success": "error", "status": 400, "message": "User Already Dislike Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.filter(user=ab)

                    obj.is_like = False
                    # obj.save(update_fields=("is_like",))
                    obj.update()

            if request.data['flag'] == '3':
                obj = UserMatchProfile.objects.filter(
                    like_profile_user=like_profile_user)
                obj = obj[0].id
                objs = UserMatchProfile.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True, "message": "User Dislike !", "status": 200}, status=status.HTTP_200_OK)

            # serializer.save()

            return Response({"success": True, "status": 201, "message": "Match Profile Data", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400, "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class UserSearchFilterApiView(ListAPIView):
    serializer_class = UserSeachFilterSerializer
    permission_classes = [IsAuthenticated, ]
    page_size = 2

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """

    #     user_id = self.request.user.id
    #     user_info = User.objects.filter(id=user_id)

    #     today = date.today()
    #     last_week = today - timedelta(days=5)

    #     if 'min_age' in self.request.GET:
    #         min_age = self.request.GET['min_age']
    #         current = now().date()
    #         min_date = date(current.year - int(min_age),
    #                         current.month, current.day)

    #     if 'max_age' in self.request.GET:
    #         max_age = self.request.GET['max_age']
    #         current = now().date()
    #         max_date = date(current.year - int(max_age),
    #                         current.month, current.day)

    #         return User.objects.filter(birth_date__gte=max_date,
    #                                    birth_date__lte=min_date).order_by("birth_date")

    #     # user = self.request.user

    #     user_data = User.objects.filter(
    #         Q(gender=user_info[0].interest_in) |
    #         Q(interest_in=user_info[0].gender) |
    #         Q(city=user_info[0].city) |
    #         Q(location=user_info[0].location) |
    #         Q(passion__in=user_info[0].passion.all()) |
    #         Q(idealmatch__in=user_info[0].idealmatch.all()) |
    #         Q(marital_status=user_info[0].marital_status) |
    #         Q(create_at__range=(last_week, today))).exclude(id=user_info[0].id).distinct()

    #     return user_data

    def get(self, request,  format=None):
        page_size = 10
        user_id = request.user.id
        # user_info = User.objects.filter(id=user_id)
        user_info = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id= %s", [user_id])
        # print("dffweasfewffgwefwe", people[0].name, people[0].age)
        user_passion = []

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

        # people = User.objects.raw(
        #     "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user")
        # print("people", people[0].id)
        # for p in people:

        #     print(" is ", p.id, p.age)

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
        # new_data = User.objects.filter(birth_date__range=(
        #     user_info[0].birth_date.year - 10, user_info[0].birth_date.year + 10)).exclude(id=user_info[0].id).distinct()
        # print(new_data)
        dat = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(new_data, request)

        serializer = UserSeachFilterSerializer(result_page, context={
            'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)
        # serializer = UserSeachFilterSerializer(new_data, many=True)

        # return Response({"success": True, "status": 200, "message": "Match Profile Data", "data": serializer.data, "data_count": len(serializer.data)},
        # status = status.HTTP_200_OK)
