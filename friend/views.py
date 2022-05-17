
from array import array
from logging import exception
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date, timedelta

from rest_framework.views import *
from rest_framework.viewsets import *
from rest_framework.generics import *
from rest_framework.permissions import *

from account.models import *
from account.serializers import *
from .serializers import *
from .models import *

today = date.today()
last_week = today - timedelta(days=5)


class AddFriendRequestSendView(GenericAPIView):
    serializer_class = GetFriendRequestSerializer
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(

        operation_summary="Send Friend Request Api ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'friend': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add Friend Id'),
            }),

        tags=['Friend']
    )
    def post(self, request, format='json'):
        serializer = FriendRequestSerializer(data=request.data)
        print(request.data)
        flag = request.data['flag']
        flag = str(flag)
        if serializer.is_valid():
            friend = serializer.validated_data['friend']
            users = str(request.user.id)
            user = User.objects.get(id=users)
            if flag == '1':
                if FriendRequest.objects.filter(friend=friend, user=user):
                    return Response({"success": True, "message": "Friend Request  Was Already Sent!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
                else:
                    obj = FriendRequest.objects.create(
                        user=user, friend=friend, friendrequestsent=True)
                    return Response({"success": True, "message": "Friend Request Sent!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)

            if flag == '2':
                if FriendRequest.objects.filter(friend=friend, user=user):
                    obj = FriendRequest.objects.filter(friend=friend)
                    obj = obj[0].id
                    objs = FriendRequest.objects.filter(id=obj)
                    objs.delete()
                    return Response({"success": True, "message": "Cencal Friend Request !", "status": 200}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": True, "message": "No Request !", "status": 200}, status=status.HTTP_200_OK)
        else:
            return Response({"success": True, "message": "Try again!", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddFriendRequestAcceptView(GenericAPIView):
    serializer_class = FriendListSerializer
    permission_classes = [AllowAny, ]

    def get(self, request):
        friend_list = FriendList.objects.all()
        serializer = FriendListSerializer(friend_list, many=True)
        return Response({"success": True, "message": " User Accept Request Detail", "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():

            to_user = serializer.validated_data['user']
            send_request = FriendRequest.objects.filter(friend=to_user)
            send_request.update(friendrequestsent=False)

            serializer.save()

            return Response({"success": True, "message": "Friend Request Accepted!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Friend Request was Already Accepted !", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetFriendRequestListView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendRequestListSerializer
    """
    Retrieve, update or delete a Get Follower instance.

    """
    @swagger_auto_schema(
        operation_summary="Get Send Friend Request Api By User ID ",
        tags=['Friend']
    )
    def get(self, request, user_id, format=None):
        import pdb
        pdb.set_trace()
        user_req_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(Q(
            passion__in=user_data[0].passion.all()) |
            Q(create_at__range=(last_week, today)) and
            Q(is_complete_profile=True)
        ).exclude(id=request.user.id)
        list_suggested = []
        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(user_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(
                    user_id=list_suggested[0])
                if not friend_value:
                    list_suggested
                else:
                    list_suggested.remove(friend_value[0].user_id)

        # friend_req_list = FriendRequest.objects.filter(user_id=user_id)
        friend_req_list = FriendRequest.objects.filter(
            friend_id=user_id).order_by('created_at')
        # user_suggest_friend = User.objects.filter(id__in=list_suggested)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

        # user_data = UserFriendSerializer(user_suggest_friend, many=True)
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
                                             'request': user_req_id}, many=True)
        serializer = FriendRequestListSerializer(friend_req_list, many=True)
        return Response({"success": True, "status": 200, "message": "Detail", "data": serializer.data, 'data_count': len(serializer.data), 'suggest_friend_data': user_data.data}, status=status.HTTP_200_OK)


class GetFriendRequestListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendRequestListSerializer
    """
    Retrieve, update or delete a Get Follower instance.

    """

    def get_serializer_context(self):

        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    @swagger_auto_schema(
        operation_summary="Get Send Friend Request Api By User ID ",
        tags=['Friend']
    )
    def get(self, request, format=None):
        # import pdb
        # pdb.set_trace()
        user_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(Q(gender=user_data[0].gender) |

                                        Q(passion__in=user_data[0].passion.all(
                                        ))
                                        and Q(is_complete_profile=True)

                                        ).exclude(id=request.user.id).distinct()
        list_suggested = []
        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(friend_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(
                    friend_id__in=list_suggested, user_id=user_id)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friend_id)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(user_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(
                    user_id__in=list_suggested, friend_id=user_id)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):
                        list_suggested.remove(
                            friend_value[frnd_lst_id].user_id)

        for friend_req_id in range(len(list_suggested)):

            if FriendList.objects.filter(user_id__in=list_suggested):
                friend_value = FriendList.objects.filter(user_id=user_id,
                                                         friends_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):
                        list_suggested.remove(
                            friend_value[frnd_lst_id].friends_id)

        # friend_req_list = FriendRequest.objects.filter(user_id=user_id)
        friend_req_list = FriendRequest.objects.filter(
            friend_id=user_id).order_by('-create_at')
        # user_suggest_friend = User.objects.filter(id__in=list_suggested)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])
        # user_data = UserFriendSerializer(user_suggest_friend, many=True)
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
                                             'request': user_id}, many=True)
        serializer = FriendRequestListSerializer(friend_req_list, many=True)
        return Response({"success": True, "status": 200, "message": "Get Friend Request List!", "data": serializer.data,
                         'data_count': len(serializer.data), 'suggest_friend_data': user_data.data},
                        status=status.HTTP_200_OK)


# send req -by user
class SendRequestByUserApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SendRequestListSerializer
    """
    Retrieve, API for Send Request By User instance.

    """
    @swagger_auto_schema(
        operation_summary="Get Send Friend Request Api By User ID ",
        tags=['Friend']
    )
    def get(self, request, format=None):

        user_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(Q(
            passion__in=user_data[0].passion.all()) |
            Q(create_at__range=(last_week, today)) and
            Q(is_complete_profile=True)
        ).exclude(id=user_id).distinct()
        list_suggested = []

        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(friend_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(user_id=user_id,
                                                            friend_id__in=list_suggested)
                if not friend_value:

                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friend_id)

        for friend_req_id in range(len(list_suggested)):

            if FriendList.objects.filter(user_id__in=list_suggested):
                friend_value = FriendList.objects.filter(user_id=user_id,
                                                         friends_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friends_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)

        # obj1 = tuple(list_suggested)

        # user_suggest_friend = User.objects.filter(
        #     id__in=list_suggested).exclude(id=request.user.id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

        # user_data = UserFriendSerializer(user_suggest_friend, many=True)
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
                                             'request': user_id}, many=True)
        friend_req_list = FriendRequest.objects.filter(
            user_id=user_id).order_by('-create_at')
        serializer = SendRequestListSerializer(friend_req_list, many=True)

        return Response({"success": True, "status": 200, "message": "Detail", "data": serializer.data,
                         'data_count': len(serializer.data), 'suggest_friend_data': user_data.data,
                         },
                        status=status.HTTP_200_OK)


class AddFriendRequestAcceptDeatilApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendListSerializer
    # @swagger_auto_schema(
    #
    #     operation_summary = "Get Friend Request Accept Api",
    #
    #     tags = ['Friend']
    # )
    # def get(self, request):
    #     friend_list = FriendList.objects.all()
    #     serializer = FriendListSerializer(friend_list, many=True)
    #     return Response(
    #         {"success": True, "message": " User Accept Request Detail", "status": 200, "data": serializer.data},
    #         status=status.HTTP_200_OK)

    @ swagger_auto_schema(

        operation_summary="Friend Request Accept Post Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
                'friend': openapi.Schema(type=openapi.TYPE_STRING, description='Add Friend Id'),
            }),

        tags=['Friend']
    )
    def post(self, request, format='json'):

        flag = str(request.data['flag'])
        serializer = FriendListSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():

            users = str(request.user.id)
            user = User.objects.get(id=users)
            friends = serializer.validated_data['friends']

            if flag == '1':  # add friend

                if FriendList.objects.filter(user=user, friends=friends, is_accepted=True):
                    return Response({"success": "error", "status": 400, "message": "User Already friend"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_friend = FriendList.objects.create(
                        user=user, friends=friends, is_accepted=True)
                    obj_friend = FriendList.objects.create(
                        user=friends, friends=user, is_accepted=True)
                    # obj = FriendRequest.objects.filter(
                    #     friend=user, user=friends)
                    if FriendRequest.objects.filter(
                            friend=user, user=friends):
                        obj = FriendRequest.objects.filter(
                            friend=user, user=friends)
                        print("if:", obj)
                    else:
                        obj = FriendRequest.objects.filter(
                            friend=friends, user=user)
                        print("ELSE :", obj)
                    obj = obj[0].id
                    objs = FriendRequest.objects.filter(id=obj)
                    objs.delete()

            if flag == '2':  # delete  request
                if FriendRequest.objects.filter(
                        friend=user, user=friends):
                    obj = FriendRequest.objects.filter(
                        friend=user, user=friends)
                    print("if :", obj)
                else:
                    obj = FriendRequest.objects.filter(
                        friend=friends, user=user)
                    print("else :", obj)
                if obj:
                    obj = obj[0].id
                    objs = FriendRequest.objects.filter(id=obj)
                    objs.delete()
                    return Response({"success": True, "message": "Friend Request Deleted !", "status": 200}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": True, "message": "No Data", "status": 200}, status=status.HTTP_200_OK)
            if flag == '3':  # unfriend user
                if FriendList.objects.filter(friends=friends):
                    obj = FriendList.objects.filter(friends=friends, user=user)

                    obj = obj[0].id
                    objs = FriendList.objects.filter(id=obj)
                    objs.delete()
                    obj1 = FriendList.objects.filter(
                        user=friends, friends=user)

                    obj1 = obj1[0].id
                    objs1 = FriendList.objects.filter(id=obj1)
                    objs1.delete()
                    return Response({"success": True, "status": 200, "message": "User  Unfriend"}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": "error", "status": 400, "message": "User Already Unfriend"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # serializer.save()

            return Response(
                {"success": True, "message": "Friend Request Accepted!",
                    "status": 201, "data": serializer.data},
                status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": " Try Again!", "status": 400,
                             "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetFriendRequestAcceptApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendRequestAcceptSerializer
    """
    Retrieve API FOR Friend Accept List.
    """

    def get_object(self, user_id):
        try:
            return FriendList.objects.filter(user_id=user_id)
        except FriendList.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary="Get Friend Request Accept Api",

        tags=['Friend']
    )
    def get(self, request, user_id, format=None):

        user_req_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(
            Q(city=user_data[0].city) |
            Q(passion__in=user_data[0].passion.all()) |
            Q(create_at__range=(last_week, today)) and
            Q(is_complete_profile=True)
        ).exclude(id=user_id).distinct()

        list_suggested = []
        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(friend_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(user_id=user_id,
                                                            friend_id__in=list_suggested)

                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friend_id)

        for friend_req_id in range(len(list_suggested)):

            if FriendList.objects.filter(friends_id__in=list_suggested):
                friend_value = FriendList.objects.filter(user_id=user_id,
                                                         friends_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):
                        list_suggested.remove(
                            friend_value[frnd_lst_id].friends_id)

        def get_serializer_context(self):

            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self
            }

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_friend = User.objects.filter(
        #     id__in=list_suggested).exclude(id=request.user.id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

        # user_data = UserFriendSerializer(user_suggest_friend, context={
        #                                  'request': request}, many=True)
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
                                             'request': user_req_id}, many=True)

        # user_id = request.user.id
        friend_req_list = FriendList.objects.filter(
            user_id=user_id).order_by('-create_at')
        # suggested = User.objects.all().exclude(id=user_id)[:5]

        serializer = FriendRequestAcceptSerializer(friend_req_list, many=True)
        # suggesteds = UserFriendSerializer(
        # , many=True)
        return Response({"success": True, "status": 200, "message": "User Friend List!", "data": serializer.data, 'data_count': len(serializer.data), 'suggest_friend_data': user_data.data}, status=status.HTTP_200_OK)


class GetFriendRequestAcceptApiViewV2(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendRequestAcceptSerializer
    """
    Retrieve API FOR Friend Accept List.
    """

    def get_object(self, request):
        try:
            return FriendList.objects.filter(user_id=request.user.id)
        except FriendList.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary="Get Friend Request Accept Api",

        tags=['Friend']
    )
    def get(self, request, format=None):
        user_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(

            Q(passion__in=user_data[0].passion.all())
            and Q(is_complete_profile=True)
        ).exclude(id=user_id).distinct()
        list_suggested = []

        # Q(location=user_info[0].location) |
        # Q(passion__in=user_info[0].passion.all()) |
        # ad = FriendRequest.objects.filter(user_id=list_suggested[0])
        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):

            if FriendRequest.objects.filter(friend_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(user_id=user_id,
                                                            friend_id__in=list_suggested)
                # print("fsdfswdefw", list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friend_id)

        for friend_req_id in range(len(list_suggested)):

            if FriendList.objects.filter(friends_id__in=list_suggested):
                friend_value = FriendList.objects.filter(user_id=user_id,
                                                         friends_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    for frnd_lst_id in range(len(friend_value)):

                        list_suggested.remove(
                            friend_value[frnd_lst_id].friends_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_friend = User.objects.filter(
        #     id__in=list_suggested).exclude(id=request.user.id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

        # user_data = UserFriendSerializer(user_suggest_friend, many=True)
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
                                             'request': user_id}, many=True)
        friend_req_list = FriendList.objects.filter(
            user_id=user_id).order_by('-create_at')
        # suggested = User.objects.all().exclude(id=user_id)[:5]

        serializer = FriendRequestAcceptSerializer(friend_req_list, many=True)

        # suggesteds = UserFriendSerializer(suggested, many=True)
        return Response({"success": True, "status": 200, "message": "user friends list(Accepted Friend Request)!", "data": serializer.data,
                         'data_count': len(serializer.data), 'suggest_friend_data': user_data.data},
                        status=status.HTTP_200_OK)


########################follow API########################################
class AddFollowRequestView(GenericAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated, ]

    """
    Create Follow  Request instance.

    """
    @swagger_auto_schema(

        operation_summary="Create Api For Send Follow Request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
                'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
            }),

        tags=['Follow']
    )
    def post(self, request, format='json'):
        try:

            serializer = FollowRequestSerializer(data=request.data)

            if serializer.is_valid():
                # serializer.save()
                follow = serializer.validated_data['follow']
                users = str(request.user.id)
                user = User.objects.get(id=users)
                obj = FollowRequest.objects.create(
                    user=user, follow=follow, is_follow=True)

                return Response({"success": True, "message": "Follow Request Send", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": "error",  "message": "Follow Request was Already Send", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': 'Data Not Found!',
                'status': 404},
            status=status.HTTP_404_NOT_FOUND)


class FollowRequestAcceptView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    """
    Create Follow  Accept instance.

    """

    # def get(self, request):
    #     follow_accept =FollowAccept.objects.all()
    #     serializer = FollowAcceptSerializer(follow_accept, many=True)
    #     return Response({"success": True,"message" :" User  Accept follow Detail" , "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)
    @swagger_auto_schema(

        operation_summary="Create Api For Accept Follow Request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
                'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Flag 1 for Follow and flag 2 for UnFollow'),
            }),

        tags=['Follow']
    )
    def post(self, request, format='json'):

        users = str(request.user.id)
        user = User.objects.get(id=users)
        # follow = request.data['follow']

        serializer = SendFollowRequestSerializer(data=request.data)

        if serializer.is_valid():
            # user = serializer.validated_data['user']
            follow = serializer.validated_data['follow']
            if request.data['flag'] == '1':
                if FollowRequest.objects.filter(follow=follow):
                    return Response({"success": "error", "status": 400, "message": " Already followed"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_follow = FollowRequest.objects.create(
                        user=user, follow=follow, is_follow=True)

            if request.data['flag'] == '2':
                obj = FollowRequest.objects.filter(follow=follow)
                obj = obj[0].id
                objs = FollowRequest.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True, "message": "user UnFollow ", "status": 200},
                                status=status.HTTP_200_OK)

            return Response({"success": True, "message": "Send Follow Request!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "NO data Found", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetFollowingApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowRequestFollowingSerializer
    """
    Retrieve,  Get Followering instance.

    """

    # def get_object(self, user_id):
    #     try:
    #         return FollowRequest.objects.filter(user_id=user_id)
    #     except FollowRequest.DoesNotExist:
    #         raise Http404
    @swagger_auto_schema(

        operation_summary="Get Following Api",

        tags=['Follow']
    )
    def get(self, request, user_id, format=None):
        user_req_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(

            Q(passion__in=user_data[0].passion.all())
            and Q(is_complete_profile=True)
        ).exclude(id=user_id).distinct()
        list_suggested = []

        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for follow_list_id in range(len(list_suggested)):

            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(user_id=user_id,
                                                            follow_id__in=list_suggested)

                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):

                        list_suggested.remove(
                            follow_value[flw_lst_id].follow_id)

        for follow_req_id in range(len(list_suggested)):

            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(follow_id=user_id,
                                                            user_id__in=list_suggested)
                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):

                        list_suggested.remove(
                            follow_value[flw_lst_id].user_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_follow = User.objects.filter(
        #     id__in=list_suggested).exclude(id=user_id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_follow = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

        # user_data = UserFriendSerializer(user_suggest_follow, many=True)
        user_data = UserSuggestionSerializer(user_suggest_follow, context={
            'request': user_id}, many=True)
        # user_req_id

        follower_info = FollowRequest.objects.filter(
            user_id=user_id).order_by('-create_at')
        serializer = FollowRequestFollowingSerializer(follower_info, many=True)
        return Response({"success": True,
                         "message": " User following Detail",
                        "data": serializer.data,
                         "status": 200,
                         'data_count': len(serializer.data),
                         "follow_suggestion": user_data.data
                         }, status=status.HTTP_200_OK)


# GetFollowerView
class GetFollowerFollowingView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = FollowRequestFollowingSerializer
    """
    Retrieve Get Followering instance.

    """

    # def get_object(self, user_id):
    #     try:
    #         return FollowRequest.objects.filter(user_id=user_id)
    #     except FollowRequest.DoesNotExist:
    #         raise Http404
    @swagger_auto_schema(

        operation_summary="Get Following Api",

        tags=['Follow']
    )
    def get(self, request,  user_id, format=None):
        try:
            user_req_id = request.user.id
            user_data = User.objects.filter(id=user_id)
            user_data = User.objects.filter(
                Q(city=user_data[0].city) |
                Q(gender=user_data[0].gender) |
                Q(idealmatch__in=user_data[0].idealmatch.all()) |
                Q(passion__in=user_data[0].passion.all()) and
                Q(is_complete_profile=True)).exclude(id=user_id).distinct()
            list_suggested = []

            for user_list_id in range(len(user_data)):
                fetch_data = user_data[user_list_id].id
                list_suggested.append(fetch_data)

            for follow_list_id in range(len(list_suggested)):

                if FollowRequest.objects.filter(follow_id__in=list_suggested):
                    follow_value = FollowRequest.objects.filter(user_id=user_id,
                                                                follow_id__in=list_suggested)

                    if not follow_value:
                        list_suggested
                    else:
                        for flw_lst_id in range(len(follow_value)):
                            list_suggested.remove(
                                follow_value[flw_lst_id].follow_id)

            for follow_req_id in range(len(list_suggested)):

                if FollowRequest.objects.filter(follow_id__in=list_suggested):
                    follow_value = FollowRequest.objects.filter(follow_id=user_id,
                                                                user_id__in=list_suggested)
                    if not follow_value:
                        list_suggested
                    else:
                        for flw_lst_id in range(len(follow_value)):

                            list_suggested.remove(
                                follow_value[flw_lst_id].user_id)

            # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
            # user_suggest_follow = User.objects.filter(
            #     id__in=list_suggested).exclude(id=user_id)
            list_suggesteds = tuple(list_suggested)
            user_suggest_follow = User.objects.raw(
                "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])
            # user_data = UserFriendSerializer(user_suggest_follow, many=True)
            user_data = UserSuggestionSerializer(user_suggest_follow, context={
                'request': user_id}, many=True)
            follower_info = FollowRequest.objects.filter(
                user_id=user_id).order_by('-create_at')
            serializer = FollowRequestFollowingSerializer(
                follower_info, many=True)
            return Response({"success": True,
                            "message": " User following Detail",
                             "data": serializer.data,
                             "status": 200,
                             'data_count': len(serializer.data),
                             "follow_suggestion": user_data.data
                             },
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': 'Not Data Found',
                'status': 404, },
            status=status.HTTP_404_NOT_FOUND)


class GetFollowerApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowRequestFollowerV2Serializer
    """
    Retrieve,  Get Follower instance API .

    """
    @swagger_auto_schema(

        operation_summary="Get Follower Api",

        tags=['Follow']
    )
    def get(self, request,  user_id, format=None):
        user_req_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(
            Q(city=user_data[0].city) |
            Q(gender=user_data[0].gender) |
            Q(passion__in=user_data[0].passion.all()) and
            Q(is_complete_profile=True)).exclude(id=user_id).distinct()
        list_suggested = []

        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for follow_list_id in range(len(list_suggested)):
            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(user_id=user_id,
                                                            follow_id__in=list_suggested)
                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):
                        list_suggested.remove(
                            follow_value[flw_lst_id].follow_id)

        for follow_req_id in range(len(list_suggested)):

            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(follow_id=user_id,
                                                            user_id__in=list_suggested)
                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):

                        list_suggested.remove(
                            follow_value[flw_lst_id].user_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_follow = User.objects.filter(
        #     id__in=list_suggested).exclude(id=user_id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_follow = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])
        user_data = UserSuggestionSerializer(user_suggest_follow, context={
            'request': user_id}, many=True)
        # user_data = UserFriendSerializer(user_suggest_follow, many=True)
        follower_info = FollowRequest.objects.filter(
            follow_id=user_id).order_by('-create_at')
        serializer = FollowRequestFollowerV2Serializer(
            follower_info, many=True)
        return Response({"success": True,
                        "message": " User follower Detail",
                         "data": serializer.data,
                         "status": 200,
                         "data_count": len(serializer.data),
                         "follow_suggestion": user_data.data

                         }, status=status.HTTP_200_OK)


class GetFollowersView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = FollowRequestFollowerV2Serializer
    """
    Retrieve, update or delete a Get Follower instance.

    """

    # def get_object(self, user_id):
    #     try:
    #         return FollowRequest.objects.filter(follow_id=user_id)
    #     except FollowRequest.DoesNotExist:
    #         raise Http404    # def get_object(self, user_id):
    #     try:
    #         return FollowRequest.objects.filter(follow_id=user_id)
    #     except FollowRequest.DoesNotExist:
    #         raise Http404    # def get_object(self, user_id):
    #     try:
    #         return FollowRequest.objects.filter(follow_id=user_id)
    #     except FollowRequest.DoesNotExist:
    #         raise Http404

    @ swagger_auto_schema(

        operation_summary="Get Follower Api",

        tags=['Follow']
    )
    def get(self, request,  user_id, format=None):

        follower_info = FollowRequest.objects.filter(
            follow_id=user_id).order_by('-create_at')
        serializer = FollowRequestFollowerV2Serializer(
            follower_info, many=True)
        return Response({"success": True, "message": " User follower Detail", "data": serializer.data, "status": 200,
                         'data_count': len(serializer.data)}, status=status.HTTP_200_OK)
# Get Following View


class GetFollowingView(GenericAPIView):  # temperly stop
    permission_classes = [AllowAny, ]
    QuerySet = FollowAccept.objects.all()
    serializer_class = FollowListFollowingSerializer
    """
    Retrieve, update or delete a Get Follower instance.
    """

    def get_object(self, user_id):
        try:
            return FollowAccept.objects.filter(user_id=user_id).order_by('-create_at')
        except FollowAccept.DoesNotExist:
            raise Http404

    @ swagger_auto_schema(

        operation_summary="Get Following Api",

        tags=['Follow']
    )
    def get(self, request, user_id, format=None):
        following_list = self.get_object(user_id)

        serializer = FollowListFollowingSerializer(following_list, many=True)

        return Response({"success": True, "message": " User Following Detail", "status": 200, "data": serializer.data, 'data_count': len(serializer.data)}, status=status.HTTP_200_OK)


class SendFollowRequestView(GenericAPIView):

    serializer_class = SendFollowRequestSerializer
    permission_classes = [IsAuthenticated, ]

    @ swagger_auto_schema(

        operation_summary="Create Api For Send Follow Request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

                'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
            }),

        tags=['Follow']
    )
    def post(self, request, format='json'):
        users = str(request.user.id)
        user = User.objects.get(id=users)

        if "flag" in request.data:
            flag = request.data['flag']
            flag = str(flag)
            serializer = SendFollowRequestSerializer(data=request.data)
            if serializer.is_valid():
                follow = serializer.validated_data['follow']
                # users = str(request.user.id)
                # user = User.objects.get(id=users)
                if flag == '1':  # accept follow
                    if FollowRequest.objects.filter(follow=follow, user=user):
                        return Response({"success": True, "message": "  Already follow ", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
                    else:
                        obj = FollowRequest.objects.create(
                            user=user, follow=follow)
                        return Response({"success": True, "message": "follow Sent!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)

                if flag == '2':  # cancel follow request
                    if FollowRequest.objects.filter(follow=follow, user=user):

                        #     obj_follow_data = FollowRequest.objects.filter(
                        #         follow=user, user=follow)
                        # else:
                        obj_follow_data = FollowRequest.objects.filter(
                            follow=follow, user=user)
                        obj_follow_datas = obj_follow_data[0]
                        obj_follow_datas.is_follow = False
                        obj_follow_datas.save(update_fields=["is_follow"])

                        obj = FollowRequest.objects.filter(follow=follow)
                        obj = obj[0].id
                        objs = FollowRequest.objects.filter(id=obj)
                        objs.delete()
                        return Response({"success": True, "message": "Cancel follow Request !", "status": 200}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success": True, "message": "No Request !", "status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"success": True, "message": "No data", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": True, "message": "Flag Not Found !", "status": 200}, status=status.HTTP_200_OK)


class FollowBackApiView(GenericAPIView):

    serializer_class = FollowBackSerializer
    permission_classes = [IsAuthenticated, ]

    @ swagger_auto_schema(

        operation_summary="Create Api For Send Follow Request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

                'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
            }),

        tags=['Follow']
    )
    def post(self, request, format='json'):

        users = str(request.user.id)
        user = User.objects.get(id=users)
        if "flag" in request.data:
            flag = request.data['flag']
            flag = str(flag)
            serializer = FollowBackSerializer(data=request.data)
            if serializer.is_valid():
                follow = serializer.validated_data['follow']
                is_follow = serializer.validated_data['is_follow']

                if flag == '1':  # follow
                    if FollowRequest.objects.filter(follow=follow, user=user):
                        return Response({"success": True, "message": "Already follow Back!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
                    else:
                        obj = FollowRequest.objects.create(
                            user=user, follow=follow, is_follow=is_follow)
                        objs = FollowRequest.objects.filter(
                            user=follow, follow=user)

                        fetch_obj_data = objs[0]
                        fetch_obj_data.is_follow = True
                        fetch_obj_data.save(update_fields=["is_follow"])

                        return Response({"success": True, "message": "Follow Back added!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)

                if flag == '2':  # remove follow back
                    if FollowRequest.objects.filter(follow=follow, user=user):
                        obj = FollowRequest.objects.filter(
                            follow=follow, user=user)
                        objs = FollowRequest.objects.filter(
                            user=follow, follow=user)
                        fetch_obj_data = objs[0]
                        fetch_obj_data.is_follow = False
                        fetch_obj_data.save(update_fields=["is_follow"])

                        ob_set_data = FollowRequest.objects.filter(
                            id=obj[0].id)
                        ob_set_data.delete()
                        return Response({"success": True, "message": "Cancel Follow Back !", "status": 200}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success": True, "message": "No Request !", "status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"success": True, "message": "Try Again", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
        else:
            return Response({"success": True, "message": "Flag Not Found", "status": 200, }, status=status.HTTP_200_OK)


class GetFollowBackApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetFollowBackSerializer
    """
    Retrieve,  a Get Follow Back instance.

    """
    @ swagger_auto_schema(

        operation_summary="Get Follow Back Api",
        tags=['Follow']
    )
    def get(self, request, format=None):
        user_id = request.user.id

        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(Q(gender=user_data[0].gender) |
                                        Q(city=user_data[0].city) |
                                        Q(idealmatch__in=user_data[0].idealmatch.all()) |
                                        Q(marital_status=user_data[0].marital_status) |
                                        Q(passion__in=user_data[0].passion.all(
                                        ))
                                        and Q(is_complete_profile=True)
                                        ).exclude(id=user_id).distinct()
        list_suggested = []

        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for follow_list_id in range(len(list_suggested)):

            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(user_id=user_id,
                                                            follow_id__in=list_suggested)
                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):
                        list_suggested.remove(
                            follow_value[flw_lst_id].follow_id)

        for follow_req_id in range(len(list_suggested)):
            if FollowRequest.objects.filter(follow_id__in=list_suggested):
                follow_value = FollowRequest.objects.filter(follow_id=user_id,
                                                            user_id__in=list_suggested)
                if not follow_value:
                    list_suggested
                else:
                    for flw_lst_id in range(len(follow_value)):
                        list_suggested.remove(
                            follow_value[flw_lst_id].user_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_follow = User.objects.filter(
        #     id__in=list_suggested).exclude(id=request.user.id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_follow = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])
        # user_data = UserFriendSerializer(user_suggest_follow, many=True)
        user_data = UserSuggestionSerializer(user_suggest_follow, context={
            'request': user_id}, many=True)

        follower_info = FollowRequest.objects.filter(
            user_id=user_id).order_by('-create_at')
        serializer = GetFollowBackSerializer(follower_info, many=True)
        return Response({"success": True,
                        "message": " User Follow Back",
                         "data": serializer.data,
                         "status": 200,
                         'data_count': len(serializer.data),
                         "follow_suggestion": user_data.data,
                         }, status=status.HTTP_200_OK)

# for testing suggested friend


class GetFriendRequestAcceptViewTesting(GenericAPIView):  # not use in app
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendRequestAcceptSerializer
    """
    Retrieve API FOR Friend Accept List.
    """

    def get_object(self, user_id):
        try:
            return FriendList.objects.filter(user_id=user_id)
        except FriendList.DoesNotExist:
            raise Http404

    @ swagger_auto_schema(
        operation_summary="Get Friend Request Accept Api",
        tags=['Friend']
    )
    def get(self, request, user_id, format=None):

        # user_req_id = request.user.id

        user_data = User.objects.filter(id=user_id)
        user_data = User.objects.filter(Q(passion__in=user_data[0].passion.all()) |
                                        Q(gender=user_data[0].gender) |
                                        Q(city=user_data[0].city) |
                                        Q(marital_status=user_data[0].marital_status)
                                        and Q(is_complete_profile=True)).exclude(id=user_id).distinct()

        list_suggested = []
        for user_list_id in range(len(user_data)):
            fetch_data = user_data[user_list_id].id
            list_suggested.append(fetch_data)

        for friend_list_id in range(len(list_suggested)):
            if FriendRequest.objects.filter(friend_id__in=list_suggested):
                friend_value = FriendRequest.objects.filter(user_id=user_id,
                                                            friend_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    list_suggested.remove(
                        friend_value[0].friend_id)

        for friend_req_id in range(len(list_suggested)):
            if FriendList.objects.filter(friends_id__in=list_suggested):
                friend_value = FriendList.objects.filter(user_id=user_id,
                                                         friends_id__in=list_suggested)
                if not friend_value:
                    list_suggested
                else:
                    list_suggested.remove(
                        friend_value[0].friends_id)

        # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
        # user_suggest_friend = User.objects.filter(
        #     id__in=list_suggested).exclude(id=request.user.id)
        list_suggesteds = tuple(list_suggested)
        user_suggest_friend = User.objects.raw(
            "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])
        user_data = UserSuggestionSerializer(user_suggest_friend, context={
            'request': user_id}, many=True)

        friend_req_list = FriendList.objects.filter(
            user_id=user_id).order_by('-create_at')
        # suggested = User.objects.all().exclude(id=user_id)[:5]

        serializer = FriendRequestAcceptSerializer(friend_req_list, many=True)
        # suggesteds = UserFriendSerializer(suggested, many=True)
        return Response({"success": True, "status": 200, "message": "User Friend List!", "data": serializer.data, 'data_count': len(serializer.data), 'suggest_friend_data': user_data.data}, status=status.HTTP_200_OK)


# class NewFollowBackApiView(GenericAPIView):

#     serializer_class = FollowBackSerializer
#     permission_classes = [IsAuthenticated, ]

#     @swagger_auto_schema(

#         operation_summary="Create Api For Send Follow Request",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={

#                 'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
#             }),

#         tags=['Follow']
#     )
#     def post(self, request, format='json'):
#         users = str(request.user.id)
#         user = User.objects.get(id=users)
#         flag = request.data['flag']
#         flag = str(flag)
#         serializer = FollowBackSerializer(data=request.data)
#         if serializer.is_valid():
#             follow = serializer.validated_data['follow']
#             users = str(request.user.id)
#             user = User.objects.get(id=users)
#             if flag == '1':
#                 if FollowAccept.objects.filter(follow=follow):
#                     return Response({"success": True, "message": "Already foollow Back!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
#                 else:
#                     obj = FollowAccept.objects.create(
#                         user=user, follow=follow, is_follow_accepted=True)
#                     return Response({"success": True, "message": "Follow Back added!", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)

#             if flag == '2':
#                 if FollowAccept.objects.filter(follow=follow):
#                     obj = FollowAccept.objects.filter(follow=follow)
#                     obj = obj[0].id
#                     objs = FollowAccept.objects.filter(id=obj)
#                     objs.delete()
#                     return Response({"success": True, "message": "Cancel Follow Back !", "status": 200}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"success": True, "message": "No Request !", "status": 200}, status=status.HTTP_200_OK)
#         else:
#             return Response({"success": True, "message": "Follow  Was Already Sent!", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class GetFollowBackApiView(GenericAPIView):
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = GetFollowBackSerializer
#     """
#     Retrieve,  a Get Follow Back instance.

#     """
#     @swagger_auto_schema(

#         operation_summary="Get Follow Back Api",
#         tags=['Follow']
#     )
#     def get(self, request, format=None):
#         user_id = request.user.id
#         follower_info = FollowAccept.objects.filter(user_id=user_id)
#         serializer = GetFollowBackSerializer(follower_info, many=True)
#         return Response({"success": True, "message": " User Follow Back", "data": serializer.data, "status": 200, 'data_count': len(serializer.data)}, status=status.HTTP_200_OK)


class TestingSuggestedFollowApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetFollowBackSerializer
    """
    Retrieve,  a Get Follow Back instance.

    """
    @ swagger_auto_schema(

        operation_summary="Get Follow Back Api",
        tags=['Follow']
    )
    def get(self, request, format=None):

        try:
            user_id = request.user.id
            user_data = User.objects.filter(id=user_id)
            user_data = User.objects.filter(
                passion__in=user_data[0].passion.all()).exclude(id=user_id).distinct()
            list_suggested = []
            for user_list_id in range(len(user_data)):
                fetch_data = user_data[user_list_id].id
                list_suggested.append(fetch_data)

            for follow_list_id in range(len(list_suggested)):
                if FollowRequest.objects.filter(follow_id__in=list_suggested):
                    follow_value = FollowRequest.objects.filter(user_id=user_id,
                                                                follow_id__in=list_suggested)
                    if not follow_value:
                        list_suggested
                    else:
                        for flw_lst_id in range(len(follow_value)):
                            list_suggested.remove(
                                follow_value[flw_lst_id].follow_id)

            for follow_req_id in range(len(list_suggested)):

                if FollowRequest.objects.filter(follow_id__in=list_suggested):
                    follow_value = FollowRequest.objects.filter(follow_id=user_id,
                                                                user_id__in=list_suggested)
                    if not follow_value:
                        list_suggested
                    else:
                        for flw_lst_id in range(len(follow_value)):
                            list_suggested.remove(
                                follow_value[flw_lst_id].user_id)

            # friend_req_list = FriendRequest.objects.filter(friend_id=user_id)
            # user_suggest_follow = User.objects.filter(
            #     id__in=list_suggested).exclude(id=request.user.id)
            list_suggesteds = tuple(list_suggested)
            user_suggest_follow = User.objects.raw(
                "SELECT id, date_part('year', age(birth_date))::int as age  FROM account_user where id IN %s ", [list_suggesteds])

            user_data = UserSuggestionSerializer(user_suggest_follow, context={
                'request': user_id}, many=True)

            follower_info = FollowRequest.objects.filter(
                user_id=user_id, is_follow=True)
            serializer = GetFollowBackSerializer(follower_info, many=True)
            return Response({"success": True,
                            "message": " User Follow Back",
                             "data": serializer.data,
                             "status": 200,
                             "data_count": len(serializer.data),
                             "follow_suggestion": user_data.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {'success': False, 'message': 'no data',
                 'status': 404, },
                status=status.HTTP_404_NOT_FOUND)
