from rest_framework.generics import *
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *
from rest_framework.views import *
from .models import *
from rest_framework.viewsets import *



class AddFriendRequestSendView(GenericAPIView):
    serializer_class = GetFriendRequestSerializer
    # permission_classes = (AllowAny,)
    
   

    # def get(self, request):
    #     # import pdb;pdb.set_trace()
    #     userInterest =FriendRequest.objects.all()
    #     serializer = GetFriendRequestSerializer(userInterest, many=True)
    #     return Response({"success": True, "message" :" User  Send Request Detail" ,"status" :200,"data": serializer.data}, status=status.HTTP_200_OK)
    @swagger_auto_schema(
      
        operation_summary = "Send Friendt Request Api ",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
            'receiver': openapi.Schema(type=openapi.TYPE_STRING, description='Add Friend Id'),
        }),

        tags = ['Friend']
    )

    def post(self, request, format='json'):

        serializer = FriendRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            receiver = serializer.validated_data['receiver']
            obj = FriendRequest.objects.create(receiver=receiver, sender=sender, friendrequestsent=True)
            # serializer.save()

            return Response({"success": True, "message": "Friend Request Sent!","status":201 ,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": True, "message": "Friend Request  Was Alraedy Sent!","status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddFriendRequestAcceptView(GenericAPIView):
    serializer_class = FriendListSerializer
    # permission_classes = (AllowAny,)
   

    def get(self, request):
        friend_list =FriendList.objects.all()
        serializer = FriendListSerializer(friend_list, many=True)
        return Response({"success": True, "message" :" User Accept Request Detail" ,"status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    
    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)
        
        if serializer.is_valid(): 
        
            to_user= serializer.validated_data['user']
            send_requst = FriendRequest.objects.filter(sender =to_user )
            send_requst.update(friendrequestsent = False)
        
            serializer.save()
            
            return Response({"success": True, "message": "Friend Request Accepted!", "status": 201,"data": serializer.data }, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Friend Request was Already Accepted !","status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetFriendRequestListView(GenericAPIView):
    serializer_class = FriendRequestListSerializer
    """
    Retrieve, update or delete a Get Follower instance.

    """
    
    def get_object(self, user_id):
        try:
            return FriendRequest.objects.filter(receiver_id=user_id)
        except FriendRequest.DoesNotExist:
            raise Http404
    @swagger_auto_schema(
      
        operation_summary = "Get Send Friend Rquest Api By User ID ",
        
        tags = ['Friend']
    )

   
    def get(self, request, user_id, format=None):

        friend_req_list = self.get_object(user_id)
        serializer = FriendRequestListSerializer(friend_req_list, many=True)
        return Response({"success": True, "status": 200 ,"message": "Detail","data": serializer.data, 'data_count' :len(serializer.data),'suggest_friend_data':[]}, status=status.HTTP_200_OK)


class  AddFollowRequestView(GenericAPIView):
    serializer_class = FollowRequestSerializer
    # permission_classes = (AllowAny,)
    @swagger_auto_schema(
      
        operation_summary = "Get Follow All User Request ",
       

        tags = ['Follow']
    )
   
    def get(self, request):
        user_follow =FollowRequest.objects.all()
        serializer = FollowRequestSerializer(user_follow, many=True)
        return Response({"success": True,"status": 200,"message" :" User follow Request Detail" , "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
      
        operation_summary = "Create Api For Send Follow Request",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
            'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
        }),

        tags = ['Follow']
    )
    def post(self, request, format='json'):
        serializer = FollowRequestSerializer(data=request.data)
        
        if serializer.is_valid():   
            serializer.save()
            return Response({"success": True, "message": "Follow Request Send","status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error",  "message": "Follow Request was Already Send", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FollowRequestAcceptView(GenericAPIView):
    serializer_class = FollowAcceptSerializer
   
    # def get(self, request):
    #     follow_accept =FollowAccept.objects.all()
    #     serializer = FollowAcceptSerializer(follow_accept, many=True)
    #     return Response({"success": True,"message" :" User  Accept follow Detail" , "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)
    @swagger_auto_schema(
      
        operation_summary = "Create Api For Accept Follow Request",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
            'follow': openapi.Schema(type=openapi.TYPE_STRING, description='Add Follow Id'),
        }),

        tags = ['Follow']
    )

    def post(self, request, format='json'):
        user = request.data['user']
        follow = request.data['follow']

        serializer = FollowRequestSerializer(data=request.data)
        
        if serializer.is_valid(): 
            # to_user= serializer.validated_data['follow']
            # send_requst = FollowRequest.objects.filter(follow =to_user )
            # send_requst.update(is_active = False)
            # serializer.save()
            ab = serializer.validated_data['user']
            follow = serializer.validated_data['follow']
            if request.data['flag'] == '1':
                if FollowRequest.objects.filter(follow=follow):
                    return Response({"success": "error", "status": 400, "message": " Already followed"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_follow = FollowRequest.objects.create(user=ab, follow=follow)


            if request.data['flag'] == '2':
                obj = FollowRequest.objects.filter(follow=follow)
                obj = obj[0].id
                objs = FollowRequest.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True, "message": "Follow Request Deleted !", "status": 200},
                                status=status.HTTP_200_OK)
            
            return Response({"success": True, "message": "Follow Request Accept", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Follow Request Already","status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# GetFollowerView
class GetFollowerView(GenericAPIView):
    serializer_class = FollowRequestFollowingSerializer
    """
    Retrieve, update or delete a Get Followering instance.

    """
   
  
    def get_object(self, user_id):
        try:
            return FollowRequest.objects.filter(user_id=user_id)
        except FollowRequest.DoesNotExist:
            raise Http404
    @swagger_auto_schema(
      
        operation_summary = "Get Following Api",
      
        tags = ['Follow']
    )

    def get(self, request, user_id, format=None):
        # import pdb;pdb.set_trace()
        follower_info = self.get_object(user_id)
        serializer = FollowRequestFollowingSerializer(follower_info, many=True)
        return Response({"success": True, "message" :" User following Detail" ,"data": serializer.data,"status": 200, 'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)




class GetFollowerV2View(GenericAPIView):
    serializer_class = FollowRequestFollowerV2Serializer
    """
    Retrieve, update or delete a Get Follower instance.

    """

    def get_object(self, user_id):
        try:
            return FollowRequest.objects.filter(follow_id=user_id)
        except FollowRequest.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary="Get Follower Api",

        tags=['Follow']
    )
    def get(self, request, user_id, format=None):
        follower_info = self.get_object(user_id)
        serializer = FollowRequestFollowerV2Serializer(follower_info, many=True)
        return Response({"success": True, "message": " User follower Detail", "data": serializer.data, "status": 200,
                         'data_count': len(serializer.data)}, status=status.HTTP_200_OK)


# Get Following View
class GetFollowingView(GenericAPIView): # temperly stop
    QuerySet = FollowAccept.objects.all()
    serializer_class = FollowListFollowingSerializer
    """
    Retrieve, update or delete a Get Follower instance.
    """
    
   
    def get_object(self, user_id):
        try:
            return FollowAccept.objects.filter(user_id=user_id)
        except FollowAccept.DoesNotExist:
            raise Http404
    @swagger_auto_schema(
      
        operation_summary = "Get Following Api",

        tags = ['Follow']
    )

    def get(self, request, user_id, format=None):    
        following_list = self.get_object(user_id)
        serializer = FollowListFollowingSerializer(following_list, many=True)
        
        return Response({"success": True,"message" :" User Following Detail" , "status": 200,"data": serializer.data ,'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)


class AddFriendRequestAcceptDeatilApiView(GenericAPIView):
    serializer_class = FriendListSerializer
    @swagger_auto_schema(
      
        operation_summary = "Get Friend Request Accept Api",
        

        tags = ['Friend']
    )
    def get(self, request):
        friend_list = FriendList.objects.all()
        serializer = FriendListSerializer(friend_list, many=True)
        return Response(
            {"success": True, "message": " User Accept Request Detail", "status": 200, "data": serializer.data},
            status=status.HTTP_200_OK)
    @swagger_auto_schema(
      
        operation_summary = "Friend Request Accept Post Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
            'friend': openapi.Schema(type=openapi.TYPE_STRING, description='Add Friend Id'),
        }),

        tags = ['Friend']
    )
    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)

        if serializer.is_valid():
            # import pdb;pdb.set_trace()
            ab = serializer.validated_data['user']
            friends = serializer.validated_data['friends']
            if request.data['flag'] == '1': # add friend
                if FriendList.objects.filter(friends=friends):
                    return Response({"success": "error", "status": 400, "message": "User Already friend"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_friend = FriendList.objects.create(user = ab,friends=friends,is_accepted= True)
                    obj = FriendRequest.objects.filter(sender=friends)
                    obj = obj[0].id
                    objs = FriendRequest.objects.filter(id=obj)
                    objs.delete()

            if request.data['flag'] == '2': # delete  request
                obj = FriendRequest.objects.filter(sender=friends)
                obj = obj[0].id
                objs = FriendRequest.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True,"message": "Friend Request Deleted !" ,"status": 200},status=status.HTTP_200_OK)

            serializer.save()

            return Response(
                {"success": True, "message": "Friend Request Accepted!", "status": 201, "data": serializer.data},
                status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Friend Request was Already Accepted !", "status": 400,
                             "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GetFriendRequestAcceptView(GenericAPIView):
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
      
        operation_summary = "Get Friend Request Accept Api",
       
        tags = ['Friend']
    )

    def get(self, request, user_id, format=None):

        friend_req_list = self.get_object(user_id)
        serializer = FriendRequestAcceptSerializer(friend_req_list, many=True)
        return Response({"success": True, "status": 200 ,"message": "Friend Request Accept!","data": serializer.data, 'data_count' :len(serializer.data),'suggest_friend_data':[]}, status=status.HTTP_200_OK)

